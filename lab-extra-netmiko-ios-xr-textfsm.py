from netmiko import ConnectHandler
import json

# Cihaza bağlantı bilgileri
device = {
    'device_type': 'cisco_xr',  # Cihaz tipi
    'host': 'sandbox-iosxr-1.cisco.com',  # Cihazın adresi
    'username': 'admin',  # Kullanıcı adı
    'password': 'C1sco12345',  # Şifre
    'port': 22,  # SSH port numarası
}

# Cihaza bağlan
net_connect = ConnectHandler(**device)

# Bir komut çalıştır
output = net_connect.send_command('show ip interface brief')

# Çıktıyı yazdır
print(output)

# Bağlantıyı kapat
net_connect.disconnect()




########################################################################################################################
print('########################################################################################################################')
print('########################################################################################################################')
print('########################################################################################################################')



from netmiko import ConnectHandler

# Cihaza bağlantı bilgileri
device1 = {
    'device_type': 'cisco_xr',  # Cihaz tipi
    'host': 'sandbox-iosxr-1.cisco.com',  # Cihazın adresi
    'username': 'admin',  # Kullanıcı adı
    'password': 'C1sco12345',  # Şifre
    'port': 22,  # SSH port numarası
}

# Cihaza bağlan
net_connect1 = ConnectHandler(**device1)

# Bir komut çalıştır
output1 = net_connect1.send_command('show ip interface brief',use_textfsm=True)

# Çıktıyı yazdır
pretty_output = json.dumps(output1, indent=2)
print(pretty_output)


# Bağlantıyı kapat
net_connect1.disconnect()

