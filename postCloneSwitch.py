# title: Cisco Meraki Switch Device Cloning
# description: This script will clone a source switch to one or more target switches within the same organization.

import requests
from tqdm import tqdm

# Replace with your Meraki API key or use a default key
DEFAULT_API_KEY = 'STORE-DEFAULT-API-KEY-HERE'
MERAKI_BASE_URL = 'https://api.meraki.com/api/v1'

# Function to fetch organizations
def get_organizations(api_key):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    response = requests.get(f'{MERAKI_BASE_URL}/organizations', headers=headers)
    response.raise_for_status()
    return response.json()

# Function to fetch MS devices (switches) within an organization
def get_ms_devices(api_key, org_id):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    response = requests.get(f'{MERAKI_BASE_URL}/organizations/{org_id}/devices', headers=headers)
    response.raise_for_status()
    return [device for device in response.json() if device['model'][:2] == 'MS']

# Function to clone a switch to target devices
def clone_switch(api_key, org_id, source_serial, target_serials):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    source_device = next((device for device in get_ms_devices(api_key, org_id) if device['serial'] == source_serial), None)

    if source_device:
        print(f"Cloning source switch: {source_device['name']} ({source_device['serial']})")

        for target_serial in tqdm(target_serials, desc="Cloning Progress"):
            if target_serial != source_serial:
                payload = {
                    'name': source_device['name'],
                    'cloneFromSerial': source_device['serial'],
                    'copyPortConfigs': True,
                    'copySwitchSettings': True,
                }

                response = requests.post(f'{MERAKI_BASE_URL}/devices/{target_serial}/clone', headers=headers, json=payload)
                response.raise_for_status()
    else:
        print(f"Source switch with serial {source_serial} not found.")

# Function to list registered switches
def list_registered_switches(ms_devices):
    print('List of registered MS devices (switches):')
    for i, device in enumerate(ms_devices, start=1):
        print(f'{i}. {device["name"]} ({device["serial"]})')

# Main function
def main():
    # Banner message
    print('Cisco Meraki Switch Device Cloning Script')
    print('Developer: Mohd NeoTech <mohdneotech@gmail.com>')
    print('-----------------------------------------------')

   # Prompt for API key choice
    use_default_api_key = input('Do you want to use the default API key? (y/n): ').strip().lower()
    if use_default_api_key == 'y':
        api_key = DEFAULT_API_KEY
    else:
        api_key = input('Enter your Meraki API key: ')

    # Fetch organizations
    try:
        organizations = get_organizations(api_key)
        if not organizations:
            print('No organizations found. Please check your API key or organization permissions.')
            return
    except requests.exceptions.RequestException as e:
        print(f'Error fetching organizations: {e}')
        return

    # Prompt for organization selection
    print('Select an organization:')
    for i, org in enumerate(organizations, start=1):
        print(f'{i}. {org["name"]} ({org["id"]})')
    
    org_choice = int(input('Enter the number of the organization: '))
    if org_choice < 1 or org_choice > len(organizations):
        print('Invalid organization choice.')
        return
    
    selected_org = organizations[org_choice - 1]
    org_id = selected_org['id']

    # Fetch and list MS devices within the selected organization
    try:
        ms_devices = get_ms_devices(api_key, org_id)
        if not ms_devices:
            print('No MS devices (switches) found in the organization.')
            return
    except requests.exceptions.RequestException as e:
        print(f'Error fetching MS devices: {e}')
        return

    list_registered_switches(ms_devices)

    # Prompt for source switch selection
    source_choice = int(input('Enter the number of the source switch to clone: '))
    if source_choice < 1 or source_choice > len(ms_devices):
        print('Invalid source switch choice.')
        return
    
    source_serial = ms_devices[source_choice - 1]['serial']

    # Prompt for target switches selection (multiple)
    print('Select one or more target switches to clone to (enter 0 when done):')
    target_serials = []
    while True:
        target_choice = int(input('Enter the number of a target switch or 0 to finish: '))
        if target_choice == 0:
            break
        if target_choice < 1 or target_choice > len(ms_devices):
            print('Invalid target switch choice.')
        else:
            target_serial = ms_devices[target_choice - 1]['serial']
            target_serials.append(target_serial)

    if not target_serials:
        print('No valid target switches selected.')
        return

    # Clone switches with progress bar
    clone_switch(api_key, org_id, source_serial, target_serials)

    print('Switch cloning completed.')

if __name__ == '__main__':
    main()
