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
#                       If only one ePO server is connected to the DXL fabric
#                       this constant can be set to None (the client will
#                       automatically determine the ePO's unique identifier).
#
#       SEARCH_TEXT   : The search text to use (system name, etc.)

from __future__ import absolute_import
from __future__ import print_function
import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlbootstrap.util import MessageUtils
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

# The search text
SEARCH_TEXT = "<specify-find-search-text>"

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    # Create the ePO client
    epo_client = EpoClient(client, EPO_UNIQUE_ID)

    # Run the system find command
    res = epo_client.run_command("system.find", {"searchText": SEARCH_TEXT})

    # Load find result into list
    res_list = MessageUtils.json_to_dict(res)

    # Display the results
    print(MessageUtils.dict_to_json(res_list, pretty_print=True))
