#pip install pan-python

from pan.xapi import PanXapi
import getpass

# Get user input
panorama_ip = input("Enter Panorama IP: ")
username = input("Enter your Panorama username: ")
password = getpass.getpass("Enter your Panorama password: ")
device_group = input("Enter the device group name: ")
address_group_name = input("Enter the address group name: ")
members = input("Enter comma-separated address object names to include: ").split(',')

# Connect to Panorama
xapi = PanXapi(hostname=panorama_ip, api_username=username, api_password=password)

# Build XML for static address group
members_xml = "".join([f"<member>{m.strip()}</member>" for m in members])

element = f"""
<entry name="{address_group_name}">
    <static>
        {members_xml}
    </static>
</entry>
"""

xpath = f"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{device_group}']/address-group"

try:
    print(f"📦 Creating address group '{address_group_name}' in device group '{device_group}'...")
    xapi.set(xpath=xpath, element=element)
    print("✅ Address group created successfully.")

    # Ask to commit
    commit = input("Do you want to commit changes to Panorama? (yes/no): ").strip().lower()
    if commit == "yes":
        print("📝 Committing changes...")
        xapi.commit(cmd="<commit-all><shared-policy><device-group><entry name='{0}'/></device-group></shared-policy></commit-all>".format(device_group))
        print("✅ Commit pushed successfully.")
    else:
        print("⚠️ Changes were not committed. Please commit manually in Panorama GUI.")

except Exception as e:
    print(f"❌ Error: {e}")
