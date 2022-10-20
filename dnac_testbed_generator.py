# Module import
import os
import logging
import jinja2
from pyats import aetest
from pyats.log.utils import banner
from dotenv import load_dotenv

load_dotenv()
DEVICE_PASSWORD = os.getenv("DEVICE_PASSWORD")

# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
# ----------------
# Connected to devices
# ----------------
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        testbed.connect()

# ----------------
# Generate testbed from DNAC
# ----------------
class GenerateTestbed(aetest.Testcase):
    """Use DNAC APIs and Jinja2 to generate a pyATS Testbed"""

    @aetest.setup
    def setup(self, testbed):
        """ Testcase Setup section """
        # connect to device
        for device,device_name in testbed.devices.items():
            self.device = device_name
    
    @aetest.test
    def get_credential_data(self):
        credential_list = self.device.rest.get("/dna/intent/api/v1/device-credential/")
        # Get the JSON payload
        self.credential_data=credential_list.json()

    @aetest.test
    def get_devices_data(self):
        device_list = self.device.rest.get("/dna/intent/api/v1/network-device/")
        # Get the JSON payload
        self.device_data=device_list.json()['response']

    @aetest.test
    def setup_template(self):
        with open('template.j2', "r") as f:
            template_data = f.read()
        template = jinja2.Template(template_data)
        self.template_output = template.render(data_to_template = self.device_data, username = self.credential_data, password = DEVICE_PASSWORD)

    @aetest.test
    def generate_testbed(self):
        with open("testbed.yaml", "w") as fh:
            fh.write(self.template_output)               
            fh.close()

# ----------------
# Validate Testbed
# ----------------
class ValidateTestbed(aetest.Testcase):
    """Use pyATS Validate to validate generated testbed"""

    @aetest.test
    def validate_testbed(self):
        """ Testcase Setup section """
        # connect to device
        os.system("pyats validate testbed --testbed-file testbed.yaml")
        # Loop over devices in tested for testing
