from netmiko import ConnectHandler
# ntc template
from ntc_templates.parse import parse_output
import json

connection = ConnectHandler(
    host="sandbox-nxos-1.cisco.com",
    username="admin",
    password="Admin_1234!",
    device_type="cisco_nxos",
    port=22,
    timeout=100)

output = connection.send_command("show version")

parsed_interfaces = parse_output(
    platform="cisco_nxos",
    command="show version",
    data=output)

print(json.dumps(parsed_interfaces, indent=2))

connection.disconnect()