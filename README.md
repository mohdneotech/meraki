# Cisco Meraki API Integration with Python

The scripts interacts with the Meraki API to gather data. Follow the steps below to use the scripts.

## Prerequisites

- Python 3.x installed on your machine.
- A Meraki API key. You can obtain it from the Meraki Dashboard (https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API).
- python libraries -> requests, tqdm, tabulate. pip is the package manager for Python (https://pypi.org/project/pip/). Use following command to install for first time or new environment
   
   ``` bash
   pip install <library-name>

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/mohdneotech/meraki.git

2. Change into the repository directory:

   ```bash
   cd meraki/

3. Run the script:

   ```bash
   python <script file-name.py>

4. Follow the on-screen prompts to enter your Meraki API key and select the organization, network accordingly.

5. You may store default Meraki API key in the files to store your own key. Saves time. You'll notice the following lines in include/config.py

   ```bash
    DEFAULT_API_KEY = 'STORE-DEFAULT-API-KEY-HERE'

6. The script will retrieve and display the requested informations based on each script functions.


## Motivation

The motivation behind this project stemmed from my experience working with Cisco Meraki in various networking scenarios. I often found the need to retrieve detailed information from the dashboard navigating multiple screens, and I wanted a streamlined way to accomplish this task programmatically. This project was born out of my passion for simplifying network management and automation.

## Why I Built This Project

I built this project to provide network administrators and engineers with a convenient tool for retrieving informations from Cisco Meraki devices. It's a common task in network management, and having scripts that can do this efficiently can save time and improve the overall network administration process.

## What Did I Learn

While working on this project, I deepened my understanding of the Meraki API and Python programming. I gained experience in making HTTP requests, handling JSON data, and building a user-friendly command-line interface. Additionally, I improved my debugging and error-handling skills, which are essential in any software development project.

## Disclaimer

I created the scripts just in case anybody has same use case to retrieve informations from Meraki API. Descriptions on each scripts will be in the header of each files.

## Contributing
If you would like to contribute to this project, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
Mohd NeoTech
Email: mohdneotech@gmail.com