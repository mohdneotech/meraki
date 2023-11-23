# title: Cisco Meraki Switch Ports Information Retrieval
# description: This script will retrieve switch ports information from Meraki MS devices
#              within a network. The script will prompt for the Meraki API key and then
#              let the user choose an organization, network, and Meraki MS device.
#              The script will then retrieve the switch ports information from the selected
#              Meraki MS device and print the information in JSON format.

import requests
import json

# Default API key (you can replace this with your default key)
DEFAULT_API_KEY = 'STORE-DEFAULT-API-KEY-HERE'

# Function to retrieve a list of organizations
def get_organizations(api_key):
    BASE_URL = 'https://api.meraki.com/api/v1'
    url = f'{BASE_URL}/organizations'
    headers = {'X-Cisco-Meraki-API-Key': api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

# Function to retrieve a list of networks within an organization
def get_networks(api_key, organization_id):
    BASE_URL = 'https://api.meraki.com/api/v1'
    url = f'{BASE_URL}/organizations/{organization_id}/networks'
    headers = {'X-Cisco-Meraki-API-Key': api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

# Function to retrieve a list of Meraki MS devices within a network
def get_ms_devices(api_key, organization_id, network_id):
    BASE_URL = 'https://api.meraki.com/api/v1'
    url = f'{BASE_URL}/organizations/{organization_id}/networks/{network_id}/devices'
    headers = {'X-Cisco-Meraki-API-Key': api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

# Function to retrieve switch ports information
def get_switch_ports(api_key, organization_id, network_id, device_serial):
    BASE_URL = 'https://api.meraki.com/api/v1'
    url = f'{BASE_URL}/devices/{device_serial}/switch/ports'
    headers = {'X-Cisco-Meraki-API-Key': api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

# Function to print switch ports information in JSON format
def print_switch_ports(ports_info):
    if ports_info:
        # Convert the switch ports information to a JSON format string
        ports_json = json.dumps(ports_info, indent=4)
        print(ports_json)
    else:
        print('No switch ports information available.')

# Function to print a list of items with numbered options and get user choice
def get_user_choice(items, item_type, id_field):
    while True:
        print(f'{item_type}:')
        for i, item in enumerate(items, start=1):
            print(f'{i}. {item["name"]} ({id_field}: {item[id_field]})')
        choice = input(f'Enter the number of the {item_type} you want to select (or enter 0 to exit): ')

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(items):
                return items[choice - 1]
            elif choice == 0:
                return None
            else:
                print('Invalid choice. Please select a valid number.')
        else:
            print('Invalid input. Please enter a number.')

# Main function
def main():
    # Banner message
    print('Cisco Meraki Switch Ports Information Retrieval')
    print('Developer: Mohd NeoTech <mohdneotech@gmail.com>')
    print('-----------------------------------------------')   

    # Prompt for API key choice
    use_default_api_key = input('Do you want to use the default API key? (y/n): ').strip().lower()
    if use_default_api_key == 'y':
        api_key = DEFAULT_API_KEY
    else:
        api_key = input('Enter your Meraki API key: ')

    # Get a list of organizations
    organizations = get_organizations(api_key)

    if organizations:
        # Let the user choose an organization by its ID
        organization = get_user_choice(organizations, 'Organization', 'id')

        if organization:
            organization_id = organization['id']

            # Get a list of networks within the selected organization
            networks = get_networks(api_key, organization_id)

            if networks:
                # Let the user choose a network by its ID
                network = get_user_choice(networks, 'Network', 'id')

                if network:
                    network_id = network['id']

                    # Get a list of Meraki MS devices within the selected network
                    ms_devices = get_ms_devices(api_key, organization_id, network_id)

                    if ms_devices:
                        # Let the user choose a Meraki MS device by its serial number
                        ms_device = get_user_choice(ms_devices, 'Meraki MS Device', 'serial')

                        if ms_device:
                            device_serial = ms_device['serial']
                            print(f'Selected Meraki MS Device: {ms_device["name"]} | Model : {ms_device["model"]} | Firmware : {ms_device["firmware"]} | Serial Number: {device_serial}')

                            # Get switch ports information
                            ports_info = get_switch_ports(api_key, organization_id, network_id, device_serial)

                            if ports_info:
                                print_switch_ports(ports_info)
                            else:
                                print('Failed to retrieve switch ports information.')
                    else:
                        print('No Meraki MS devices found in the selected network.')
                else:
                    print('Exiting.')
            else:
                print('No networks found in the selected organization.')
        else:
            print('Exiting.')
    else:
        print('Failed to retrieve organizations.')

if __name__ == '__main__':
    main()
