# Module import
import requests
import os
import json
import urllib3
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

urllib3.disable_warnings()

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")
AUTH_URL = os.getenv("AUTH_URL")

template_dir = Path(__file__).resolve().parent
env = Environment(loader=FileSystemLoader(template_dir))


response = requests.post(f"{ BASE_URL }{ AUTH_URL }", auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
token = response.json()['Token']

deviceAPI = "/dna/intent/api/v1/network-device"
credentialsAPI = "/dna/intent/api/v1/device-credential/"
headers={
            "X-Auth-Token": "{}".format(token),
            "Content-type": "application/json",
        }
device_list = requests.get(f"{ BASE_URL }{ deviceAPI }", headers=headers ,verify=False)
credentials_list = requests.get(f"{ BASE_URL }{ credentialsAPI }", headers=headers ,verify=False) 

devices_template = env.get_template('template.j2')
template_output = devices_template.render(data_to_template = device_list.json()['response'], credentials = credentials_list.json())

with open("testbed.yaml", "w") as fh:
    fh.write(template_output)               
    fh.close()