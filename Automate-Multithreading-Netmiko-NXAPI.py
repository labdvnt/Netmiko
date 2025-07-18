import json
import warnings
import threading
import time
import requests
import urllib3
import base64
from netmiko import ConnectHandler
from datetime import datetime

# Uyarıları kapat
warnings.filterwarnings('ignore')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Başlangıç zamanını al
start = time.time()

# Dosya kilidi
lock = threading.Lock()

# Cihaz listesini yükle
try:
    with open('devices.json') as f:
        devices = json.load(f)
except Exception as e:
    print(f"[!] JSON dosyası okunamadı: {e}")
    exit(1)

def backup(cisco_device):
    filename = 'bütün_cihazlar_seri_no.txt'

    try:
        if cisco_device['device_type'] in ['cisco_ios', 'cisco_xe']:
            connection = ConnectHandler(**cisco_device)
            connection.enable()
            version_info = connection.send_command('show version', use_textfsm=True)

            if version_info and 'serial' in version_info[0]:
                serial = version_info[0]['serial'][0]
            else:
                serial = "SERIAL_BULUNAMADI"

            output_line = f"{cisco_device['host']} : {cisco_device['device_type']} : {serial}\n"
            connection.disconnect()
        elif cisco_device['device_type'] == 'cisco_xr':
            connection = ConnectHandler(**cisco_device)
            output = connection.send_command("show inventory", use_textfsm=True)
            connection.disconnect()

            # IOS-XR için sade kontrol
            if output and 'sn' in output[0] and output[0]['sn'] != 'N/A':
                serial = output[0]['sn']
            else:
                serial = "SERIAL_BULUNAMADI"

            output_line = f"{cisco_device['host']} : {cisco_device['device_type']} : {serial}\n"
        elif cisco_device['device_type'] == 'cisco_nxos':
            username = cisco_device['username']
            password = cisco_device['password']
            credentials = f"{username}:{password}"
            apikey = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {apikey}'
            }

            payload = {
                "ins_api": {
                    "version": "1.0",
                    "type": "cli_show",
                    "chunk": "0",
                    "sid": "1",
                    "input": "show version",
                    "output_format": "json"
                }
            }

            url = f"https://{cisco_device['host']}/ins"
            response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

            seri = response.json()['ins_api']['outputs']['output']['body']['proc_board_id']
            output_line = f"{cisco_device['host']} : {cisco_device['device_type']} : {seri}\n"

        else:
            output_line = f"{cisco_device['host']} : {cisco_device['device_type']} : DESTEKLENMEYEN_TİP\n"

        # Güvenli dosya yazımı
        with lock:
            with open(filename, 'a', encoding='utf-8') as outfile:
                outfile.write(output_line)

    except Exception as e:
        print(f"[!] {cisco_device['host']} için hata: {e}")

# Thread’leri başlat
threads = []

for device in devices:
    cisco_device = {
        'host': device['ip'],
        'username': device['username'],
        'password': device['password'],
        'device_type': device['device_type'],
        'port': device.get('port', 22),  # port belirtilmemişse 22
        'timeout': 150
    }

    # Secret varsa ekle
    if 'secret' in device:
        cisco_device['secret'] = device['secret']

    th = threading.Thread(target=backup, args=(cisco_device,))
    threads.append(th)

# Thread’leri çalıştır
for th in threads:
    th.start()

# Thread’leri bekle
for th in threads:
    th.join()

# Bitiş zamanı
end = time.time()
print(f"\n✅ Tüm işlemler tamamlandı. Toplam süre: {round(end - start, 2)} saniye.")