# title: Cisco Meraki Switch Ports Information Retrieval
# description: This script will retrieve switch ports information from Meraki MS devices

import requests

# Default API key (you can replace this with your default key)
DEFAULT_API_KEY = 'STORE-DEFAULT-API-KEY-HERE'

# Function to get the organization ID using a specified API key
def get_organization_id(api_key):
    url = 'https://api.meraki.com/api/v1/organizations'
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        organizations = response.json()
        for org in organizations:
            print(f"Org ID: {org['id']}, Org Name: {org['name']}")
        return organizations[0]['id']  # Return the first organization ID
    else:
        print(f"Failed to fetch organization ID. Status code: {response.status_code}")
        return None

# Function to get switch port information for a specific network and switch
def get_switch_port_info(api_key, org_id, network_id, switch_serial):
    url = f'https://api.meraki.com/api/v1/organizations/{org_id}/networks/{network_id}/devices/{switch_serial}/switchPorts'
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        switch_ports = response.json()
        return switch_ports
    else:
        print(f"Failed to fetch switch port information. Status code: {response.status_code}")
        return None

# Main function
def main():
    # Banner message
    print('Cisco Meraki Switch Ports Information Retrieval Script')
    print('Developer: Mohd NeoTech <mohdneotech@gmail.com>')
    print('-----------------------------------------------')

    # You can choose to use a default API key or input a custom one
    use_default_api_key = input("Use default API key? (y/n): ").lower() == 'y'

    if use_default_api_key:
        # Use your default API key here
        api_key = 'DEFAULT_API_KEY'
    else:
        # Input a custom API key
        api_key = input("Enter your custom API key: ")

    org_id = get_organization_id(api_key)
    if org_id:
        # Replace with your desired organization, network, and switch information
        network_id = 'YOUR_NETWORK_ID'
        switch_serial = 'YOUR_SWITCH_SERIAL'

        switch_ports = get_switch_port_info(api_key, org_id, network_id, switch_serial)
        if switch_ports:
            # Print or process switch port data as needed
            for switch_port in switch_ports:
                print(switch_port)

if __name__ == "__main__":
    main()
