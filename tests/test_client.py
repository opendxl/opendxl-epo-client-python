from dxlbootstrap.util import MessageUtils
from dxlepoclient import EpoClient, OutputFormat
from tests.test_base import BaseClientTest
from tests.test_value_constants import *
from tests.mock_eposerver import MockEpoServer

class TestEpoUniqueId(BaseClientTest):

    def test_inituniqueid(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            epo_client = EpoClient(dxl_client, epo_unique_id=LOCAL_TEST_SERVER_NAME)

            self.assertEqual(epo_client._epo_unique_id, LOCAL_TEST_SERVER_NAME)

    def test_initnoid(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            dxl_client.connect()

            try:
                EpoClient(dxl_client)

            except Exception as ex:
                self.assertIn("No ePO DXL services are registered with the DXL fabric", str(ex))


class TestRunCommand(BaseClientTest):

    def test_helpcommand(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            epo_client = EpoClient(
                dxl_client,
                epo_unique_id=LOCAL_TEST_SERVER_NAME + str(DEFAULT_EPO_SERVER_ID)
            )
            dxl_client.connect()

            with MockEpoServer(dxl_client):
                result = epo_client.help()

                self.assertIn(result, HELP_CMD_RESPONSE_PAYLOAD)

            dxl_client.disconnect()

    def test_runcommand(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            epo_client = EpoClient(
                dxl_client,
                epo_unique_id=LOCAL_TEST_SERVER_NAME + str(DEFAULT_EPO_SERVER_ID)
            )
            dxl_client.connect()

            with MockEpoServer(dxl_client):
                res = epo_client.run_command(
                    "system.find",
                    {"searchText": SYSTEM_FIND_CMD_NAME},
                    output_format=OutputFormat.JSON
                )

                # Load find result into dictionary
                res_list = MessageUtils.json_to_dict(res)

                self.assertEqual(res_list, SYSTEM_FIND_PAYLOAD)

            dxl_client.disconnect()


    def test_lookupidentifiers(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockEpoServer(dxl_client):
                epo_ids = EpoClient.lookup_epo_unique_identifiers(dxl_client)

                # Load find result into dictionary
                for epo_id in epo_ids:
                    self.assertIn(LOCAL_TEST_SERVER_NAME, epo_id)

            dxl_client.disconnect()
