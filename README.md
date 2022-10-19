# dnac_pyats_testbed

Python code that generates a pyATS Testbed from DNAC as a source of truth

## Requirments

- Create a Python virtual environment
- pip install requests
- pip install python-dotenv
- pip install jinja2

## Assumptions

This code assumes that all devices are using global credentials and will use the "first" set of CLI credentials for all hosts
Devices of a Software Type "Cisco Controller" will be omitted from the testbed.yaml file

## Run the code

python dnac_testbed_generator.py