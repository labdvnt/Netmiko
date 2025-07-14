import threading
import psutil
import json
import time
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException, NetmikoTimeoutException
from datetime import datetime

# Maximum number of concurrent threads
MAX_THREADS = 5  # You can change this value as needed

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
        print(f"🔹 Executing command: {command}")
        try:
            output = connection.send_command(command, use_textfsm=True)
            results[command] = output
        except Exception as e:
            results[command] = f"[COMMAND ERROR] {e}"
    return results

def write_report(outfile, device_ip, results):
    outfile.write(f"{'*' * 40}\n")
    outfile.write(f"Connected to device: {device_ip}\n")
    for command, output in results.items():
        outfile.write(f"{command.center(80, '*')}\n")
        pretty_output = json.dumps(output, indent=2) if isinstance(output, (dict, list)) else str(output)
        outfile.write(f"{pretty_output}\n\n")


def worker(device, commands_map, outfile_lock, outfile):
    print(f"\n{'=' * 50}")
    print(f"Connecting to device: {device['ip']}")
    connection = connect_to_device(device)

    if isinstance(connection, str):  # if connection is an error message
        print(f" {connection}")
        with outfile_lock:
            outfile.write(f"{connection}\n")
        return

    device_type = device['model_type']
    commands = commands_map.get(device_type, [])

    results = run_commands(connection, commands)

    with outfile_lock:
        write_report(outfile, device['ip'], results)

    connection.disconnect()


def main():
    devices = load_json_file('devices.json')
    commands_map = load_json_file('commands.json')

    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"All-Devices-Report_{timestamp}.txt"

    outfile_lock = threading.Lock()

    with open(filename, 'w') as outfile:
        active_threads = []
        for device in devices:
            while len(active_threads) >= MAX_THREADS:
                for t in active_threads:
                    if not t.is_alive():
                        active_threads.remove(t)

            t = threading.Thread(target=worker, args=(device, commands_map, outfile_lock, outfile))
            active_threads.append(t)
            t.start()

        for t in active_threads:
            t.join()

    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    print(f"\n✅ Report successfully generated: {filename}")
    print(f"📊 CPU Usage: {cpu}%")
    print(f"📊 Memory Usage: {mem}%")

    elapsed_time = time.time() - start_time
    print(f"⏱️ Total Execution Time: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    main()