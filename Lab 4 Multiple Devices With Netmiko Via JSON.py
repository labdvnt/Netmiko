import json
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException, NetmikoTimeoutException
from datetime import datetime

def load_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def connect_to_device(device):
    try:
        connection = ConnectHandler(
            ip=device['ip'],
            device_type=device['device_type'],
            port=device.get('port', 22),
            username=device['username'],
            password=device['password'],
            secret=device.get('secret', ''),
            timeout=200,
            verbose=False
        )
        if device['device_type'] in ['cisco_ios', 'cisco_xe']:
            connection.enable()
        return connection
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as auth_err:
        return f"[AUTH ERROR] {auth_err}"
    except Exception as err:
        return f"[CONNECTION ERROR] {err}"

def run_commands(connection, commands):
    results = {}
    for command in commands:
        print(f"🔹 Sending command: {command}")
        try:
            output = connection.send_command(command, use_textfsm=True)
            results[command] = output
        except Exception as e:
            results[command] = f"[COMMAND ERROR] {e}"
    return results

def write_report(outfile, device_ip, results):
    outfile.write(f"{'*' * 40}\n")
    outfile.write(f"Connecting to the device: {device_ip}\n")
    for command, output in results.items():
        outfile.write(f"{command.center(80, '*')}\n")
        pretty_output = json.dumps(output, indent=2) if isinstance(output, (dict, list)) else str(output)
        outfile.write(f"{pretty_output}\n\n")

def main():
    devices = load_json_file('devices.json')
    commands_map = load_json_file('commands.json')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"TumRapor_{timestamp}.txt"

    with open(filename, 'w') as outfile:
        for device in devices:
            print(f"\n{'=' * 50}")
            print(f"🔌 Connecting to device: {device['ip']}")
            connection = connect_to_device(device)

            if isinstance(connection, str):  # connection bir hata mesajıysa
                print(f"❌ {connection}")
                outfile.write(f"❌ {connection}\n")
                continue

            device_type = device['model_type']
            commands = commands_map.get(device_type, [])

            results = run_commands(connection, commands)
            write_report(outfile, device['ip'], results)

            connection.disconnect()

    print(f"\n✅ Rapor başarıyla oluşturuldu: {filename}")

if __name__ == '__main__':
    main()