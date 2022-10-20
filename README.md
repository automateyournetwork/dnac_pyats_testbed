# dnac_pyats_testbed

Python code that generates a pyATS Testbed from DNAC as a source of truth

## Requirments

- Create a Python virtual environment
- pip install pyats[full]
- pip install rest.connector
- pip install python-dotenv

## Assumptions

This code assumes that all devices are using global credentials and will use the "first" set of CLI credentials for all hosts
Devices of a Software Type "Cisco Controller" will be omitted from the testbed.yaml file. This will only generate the username from the Cisco DNAC Global Credentials API. 

## Global device password
As the Cisco DNAC Global credentials API encrypts the password you will need to set the DEVICE_PASSWORD environment variable, using the .env file, to set the device password within the generated testbed file.

## Run the code

pyats run job dnac_testbed_generator_job.py