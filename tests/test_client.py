from dxlbootstrap.util import MessageUtils
from dxlepoclient import EpoClient, OutputFormat
from tests.test_base import BaseEpoClientTest
from tests.test_value_constants import *
from tests.mock_eposerver import MockEpoServer

class TestEpoUniqueId(BaseEpoClientTest):

    def test_inituniqueid(self):
        with self.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            epo_client = EpoClient(dxl_client, epo_unique_id=LOCAL_TEST_SERVER_NAME)

            self.assertEqual(epo_client._epo_unique_id, LOCAL_TEST_SERVER_NAME)

    def test_initnoid(self):
        with self.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            dxl_client.connect()

            self.assertRaisesRegexp(
                Exception,
                "No ePO DXL services are registered with the DXL fabric",
                EpoClient,
                dxl_client
            )


class TestRunCommand(BaseEpoClientTest):

    def test_helpcommand(self):
        with self.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            epo_client = EpoClient(
                dxl_client,
                epo_unique_id=LOCAL_TEST_SERVER_NAME + str(DEFAULT_EPO_SERVER_ID)
            )
            mock_epo_server = MockEpoServer(dxl_client)
            dxl_client.connect()
            mock_epo_server.start_service()

            result = epo_client.help()

            self.assertIn(result, HELP_CMD_RESPONSE_PAYLOAD)

            # End test
            mock_epo_server.stop_service()
            dxl_client.disconnect()

    def test_runcommand(self):
        with self.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            epo_client = EpoClient(
                dxl_client,
                epo_unique_id=LOCAL_TEST_SERVER_NAME + str(DEFAULT_EPO_SERVER_ID)
            )
            mock_epo_server = MockEpoServer(dxl_client)
            dxl_client.connect()
            mock_epo_server.start_service()

            res = epo_client.run_command(
                "system.find",
                {"searchText": SYSTEM_FIND_CMD_NAME},
                output_format=OutputFormat.JSON
            )

            # Load find result into dictionary
            res_list = MessageUtils.json_to_dict(res)

            self.assertEqual(res_list, SYSTEM_FIND_PAYLOAD)

            # End test
            mock_epo_server.stop_service()
            dxl_client.disconnect()


    def test_lookupidentifiers(self):
        with self.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            mock_epo_server = MockEpoServer(dxl_client)
            dxl_client.connect()
            mock_epo_server.start_service()

            epo_ids = EpoClient.lookup_epo_unique_identifiers(dxl_client)

            # Load find result into dictionary
            for epo_id in epo_ids:
                self.assertIn(LOCAL_TEST_SERVER_NAME, epo_id)

            # End test
            mock_epo_server.stop_service()
            dxl_client.disconnect()
