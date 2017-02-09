# This sample invokes and displays the results of the "core help" command via
# the ePO DXL service. This displays the remote commands that are exposed by
# the ePO server.
#
# NOTE: Prior to running this sample you must provide values for the following
#       constants in this file:
#
#       EPO_UNIQUE_ID : The unique identifier used to identify the ePO server
#                       on the DXL fabric.

import json
import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlepoclient import EpoClient

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# The ePO unique identifier
EPO_UNIQUE_ID = None

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    # Create the ePO client
    epo_client = EpoClient(client, EPO_UNIQUE_ID)

    # Display the help
    print epo_client.help()
