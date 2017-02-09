# This sample invokes and displays the results of the "system find" command via
# the ePO DXL service. The results of the find command are displayed in JSON
# format.
#
# NOTE: Prior to running this sample you must provide values for the following
#       constants in this file:
#
#       EPO_UNIQUE_ID : The unique identifier used to identify the ePO server
#                       on the DXL fabric.
#
#       SEARCH_TEXT   : The search text to use (system name, etc.)

import json
import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlepoclient import EpoClient, OutputFormat

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

# The search text
#SEARCH_TEXT = "<specify-find-search-text>"
SEARCH_TEXT = "broker"

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    # Create the ePO client
    epo_client = EpoClient(client, EPO_UNIQUE_ID)

    # Run the system find command
    res = epo_client.run_command("system.find",
                                 {"searchText": SEARCH_TEXT},
                                 output_format=OutputFormat.JSON)

    # Display the results
    print json.dumps(json.loads(res, encoding='utf-8'), sort_keys=True, indent=4, separators=(',', ': '))
