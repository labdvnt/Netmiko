from netmiko import Netmiko, NetmikoAuthenticationException

device = {
    'device_type': 'cisco_ios',
    'ip': '10.103.171.68',
    'username': 'admin',     
    'password': '1234QWer!',
    'secret': '1234QWer!',
    'timeout': 100
}

commands = ['int lo1', 'ip address 1.1.1.1 255.255.255.255', 'no shut', 'exit']

connection = Netmiko(**device)
output = connection.send_command('show version', use_textfsm=True)
output2 = connection.send_config_set(commands)
output3 = connection.send_command('show ip int brief', use_textfsm=True)
print(output[0]['hostname'])
print(output2)
print(output3)

connection.disconnect()
