# title : Cisco Meraki Wireless APs and Connected Clients
# description : This script will retrieve wireless APs and count the number of connected clients
#               for each AP. The script will prompt for the Meraki API key and then let the user
#               choose an organization and network. The script will then retrieve the wireless APs
#               in the selected network and count the number of connected clients for each AP.

import requests
import include.config as config

# Default API key (you can replace this with your default key)
DEFAULT_API_KEY = config.DEFAULT_API_KEY

# Meraki base URL
BASE_URL = config.BASE_URL

# Function to retrieve a list of organizations
def get_organizations(api_key):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    url = f'{BASE_URL}/organizations'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching organizations: {e}')
        return None

# Function to retrieve a list of networks within an organization
def get_networks(api_key, org_id):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    url = f'{BASE_URL}/organizations/{org_id}/networks'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching networks: {e}')
        return None

# Function to fetch wireless APs in a network
def get_wireless_aps(api_key, network_id):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    url = f'{BASE_URL}/networks/{network_id}/devices?type=wireless'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        devices = response.json()
        return [device for device in devices if device['model'].startswith('MR')]
    except requests.exceptions.RequestException as e:
        print(f'Error fetching wireless APs: {e}')
        return None

# Function to count connected clients to each AP
def count_connected_clients(api_key, network_id, aps):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    ap_client_counts = []

    for ap in aps:
        ap_name = ap['name']
        ap_serial = ap['serial']

        url = f'{BASE_URL}/networks/{network_id}/devices/{ap_serial}/clients'

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            clients = response.json()
            connected_client_count = len(clients)
            ap_client_counts.append({'AP Name': ap_name, 'Connected Clients': connected_client_count})
        except requests.exceptions.RequestException as e:
            print(f'Error fetching connected clients for AP {ap_name}: {e}')

    return ap_client_counts

# Main function
def main():
    # Banner message
    print('Cisco Meraki Wireless APs and Connected Clients')
    print('Developer: Mohd NeoTech <mohdneotech@gmail.com>')
    print('-----------------------------------------------')    
    
    # Prompt for API key choice, press Enter to use default API key
    use_default_api_key = input('Do you want to use the default API key? (y/n): ').strip().lower()
    if use_default_api_key == 'y':
        api_key = DEFAULT_API_KEY
    else:
        api_key = input('Enter your Meraki API key: ')

    # Fetch organizations
    organizations = get_organizations(api_key)

    if organizations:
        # Display a list of organizations for the user to choose from
        print('Select an organization:')
        for i, org in enumerate(organizations, start=1):
            print(f'{i}. {org["name"]} ({org["id"]})')

        org_choice = int(input('Enter the number of the organization: '))
        if org_choice < 1 or org_choice > len(organizations):
            print('Invalid organization choice.')
            return

        selected_org = organizations[org_choice - 1]
        org_id = selected_org['id']

        # Fetch networks within the selected organization
        networks = get_networks(api_key, org_id)

        if networks:
            # Display a list of networks for the user to choose from
            print('Select a network:')
            for i, network in enumerate(networks, start=1):
                print(f'{i}. {network["name"]} ({network["id"]})')

            network_choice = int(input('Enter the number of the network: '))
            if network_choice < 1 or network_choice > len(networks):
                print('Invalid network choice.')
                return

            selected_network = networks[network_choice - 1]
            network_id = selected_network['id']

            # Fetch wireless APs in the selected network
            aps = get_wireless_aps(api_key, network_id)

            if aps:
                # Display APs and connected client counts
                print('Wireless Access Points (APs) and Connected Clients:')
                ap_client_counts = count_connected_clients(api_key, network_id, aps)

                if ap_client_counts:
                    for ap_count in ap_client_counts:
                        print(f'AP Name: {ap_count["AP Name"]}, Connected Clients: {ap_count["Connected Clients"]}')
                else:
                    print('No APs found in the network or failed to count connected clients.')
            else:
                print('No wireless APs found in the network.')
        else:
            print('No networks found in the selected organization.')
    else:
        print('No organizations found.')

if __name__ == '__main__':
    main()
