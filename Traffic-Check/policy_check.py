import csv
import getpass
from pan.xapi import PanXapi
import xml.etree.ElementTree as ET

# === Protocol Map ===
protocol_map = {"tcp": "6", "udp": "17"}

def build_test_command(source, destination, port, protocol, from_zone, to_zone):
    return f"""
    <test>
        <security-policy-match>
            <from>{from_zone}</from>
            <to>{to_zone}</to>
            <source>{source}</source>
            <destination>{destination}</destination>
            <destination-port>{port}</destination-port>
            <protocol>{protocol}</protocol>
        </security-policy-match>
    </test>
    """

def parse_result(xml_output):
    root = ET.fromstring(xml_output)
    entries = root.findall(".//entry")
    for entry in entries:
        rule_name = entry.get("name")
        action = entry.findtext("action")
        print(f"🔹 Rule Matched: {rule_name} | Action: {action}")

# === Get Firewall Connection Info ===
fw_ip = input("Enter Firewall IP: ")
username = input("Enter Read-Only Username: ")
password = getpass.getpass("Enter Password: ")
csv_file = input("Enter path to CSV file: ")

# === Connect to Firewall ===
try:
    xapi = PanXapi(hostname=fw_ip, api_username=username, api_password=password)
except Exception as e:
    print(f"❌ Failed to connect: {e}")
    exit(1)

# === Read and Process CSV ===
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            from_zone = row["Source Zone"]
            to_zone = row["Destination Zone"]
            source_ip = row["Source IP"]
            destination_ip = row["Destination IP"]
            port = row["Port"]
            protocol_name = row["Protocol"].lower()
            protocol_number = protocol_map.get(protocol_name)

            if not protocol_number:
                print(f"⚠️ Invalid protocol '{protocol_name}' in row: {row}")
                continue

            print(f"\n▶️ Checking traffic: {source_ip} → {destination_ip} on port {port}/{protocol_name}")
            test_cmd = build_test_command(source_ip, destination_ip, port, protocol_number, from_zone, to_zone)
            xapi.op(cmd=test_cmd)
            parse_result(xapi.xml_document.decode())

        except Exception as e:
            print(f"❌ Error in row {row}: {e}")
