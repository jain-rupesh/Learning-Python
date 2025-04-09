import requests
import urllib3
import getpass
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== USER INPUT ==========
panorama_ip = input("Enter Panorama IP: ")
api_key = getpass.getpass("Enter API Key: ")
device_group = input("Enter Device Group Name: ")
address_group_name = input("Enter Address Group Name to Create: ")

# Sample Address Objects (can be replaced with dynamic input or CSV)
addresses = {
    "Test-Addr-1": "10.0.1.10",
    "Test-Addr-2": "10.0.1.20"
}

base_url = f"https://{panorama_ip}/api"

# ========== FUNCTIONS ==========

def create_address(name, ip):
    xpath = f"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{device_group}']/address"
    xml_payload = f"<entry name='{name}'><ip-netmask>{ip}</ip-netmask></entry>"
    url = f"{base_url}?type=config&action=set&key={api_key}&xpath={xpath}&element={xml_payload}"

    response = requests.get(url, verify=False)
    if "<response status=\"success\"" in response.text:
        print(f"✅ Created address object '{name}' ({ip}) in device group '{device_group}'")
        return True
    else:
        print(f"❌ Failed to create address '{name}': {response.text}")
        return False

def create_address_group(group_name, members):
    member_xml = "".join([f"<member>{m}</member>" for m in members])
    xml_payload = f"""
    <entry name="{group_name}">
        <static>{member_xml}</static>
    </entry>
    """
    xpath = f"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{device_group}']/address-group"
    url = f"{base_url}?type=config&action=set&key={api_key}&xpath={xpath}&element={xml_payload}"

    response = requests.get(url, verify=False)
    if "<response status=\"success\"" in response.text:
        print(f"✅ Created address group '{group_name}' in device group '{device_group}'")
        return True
    else:
        print(f"❌ Failed to create address group '{group_name}': {response.text}")
        return False

def commit_to_panorama(dg):
    print(f"\n🚀 Committing changes to device group '{dg}'...")
    commit_xml = f"<commit-all><shared-policy><device-group><entry name='{dg}'/></device-group></shared-policy></commit-all>"
    url = f"{base_url}?type=commit&action=all&key={api_key}&cmd={commit_xml}"

    response = requests.get(url, verify=False)
    if "<response status=\"success\"" in response.text:
        print("✅ Commit initiated. Waiting for completion...")
        job_id = extract_job_id(response.text)
        if job_id:
            wait_for_job(job_id)
        else:
            print("⚠️ Commit job ID not found.")
    else:
        print(f"❌ Commit failed: {response.text}")

def extract_job_id(xml_response):
    if "<job>" in xml_response:
        start = xml_response.find("<job>") + 5
        end = xml_response.find("</job>")
        return xml_response[start:end]
    return None

def wait_for_job(job_id):
    url = f"{base_url}?type=op&cmd=<show><jobs><id>{job_id}</id></jobs></show>&key={api_key}"
    while True:
        time.sleep(5)
        response = requests.get(url, verify=False)
        if "<status>FIN" in response.text:
            print(f"✅ Commit job {job_id} completed.")
            break
        elif "<status>PEND" in response.text or "<status>ACT" in response.text:
            print(f"⏳ Commit job {job_id} still running...")
        else:
            print(f"⚠️ Unexpected commit status: {response.text}")
            break

# ========== EXECUTION ==========
created_addresses = []

for name, ip in addresses.items():
    if create_address(name, ip):
        created_addresses.append(name)

if created_addresses:
    if create_address_group(address_group_name, created_addresses):
        commit_to_panorama(device_group)
else:
    print("⚠️ No address objects created. Skipping group creation and commit.")
