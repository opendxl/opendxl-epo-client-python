from dxlbootstrap.util import MessageUtils
from dxlepoclient import EpoClient, OutputFormat
from tests.test_base import BaseClientTest
from tests.test_value_constants import *
from tests.mock_eposerver import MockEpoServer


class TestClient(BaseClientTest):

    def test_init_unique_id(self):
        with self.create_client(max_retries=0) as dxl_client:
            epo_client = EpoClient(dxl_client,
                                   epo_unique_id=LOCAL_TEST_SERVER_NAME)

            self.assertEqual(epo_client._epo_unique_id, LOCAL_TEST_SERVER_NAME)

    def test_init_no_unique_id_and_no_epo_service(self):
        with self.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            self.assertRaisesRegex(
                Exception,
                "No ePO DXL services are registered with the DXL fabric",
                EpoClient,
                dxl_client)

    def test_init_no_unique_id_and_one_epo_service(self):
        with self.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            for use_commands_service in [True, False]:
                with MockEpoServer(dxl_client,
                                   use_commands_service=use_commands_service):
                    epo_client = EpoClient(dxl_client)
                    self.assertEqual(epo_client._epo_unique_id,
                                     LOCAL_TEST_SERVER_NAME +
                                     str(DEFAULT_EPO_SERVER_ID))
                    self.assertIn("core.help", epo_client.help())

    def test_init_no_unique_id_and_multiple_epo_services(self):
        with self.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            for use_commands_service in [True, False]:
                with MockEpoServer(dxl_client, id_number=0,
                                   use_commands_service=use_commands_service), \
                     MockEpoServer(dxl_client, id_number=1,
                                   use_commands_service=use_commands_service):
                    self.assertRaisesRegex(
                        Exception,
                        "Multiple ePO DXL services are registered.*" +
                        LOCAL_TEST_SERVER_NAME + '0' + ", " +
                        LOCAL_TEST_SERVER_NAME + '1',
                        EpoClient,
                        dxl_client)

    def test_lookup_epo_unique_identifiers(self):
        with self.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            for use_commands_service in [True, False]:
                with MockEpoServer(dxl_client,
                                   use_commands_service=use_commands_service):
                    epo_ids = EpoClient.lookup_epo_unique_identifiers(
                        dxl_client)
                    self.assertEqual(
                        {LOCAL_TEST_SERVER_NAME + str(DEFAULT_EPO_SERVER_ID)},
                        epo_ids)

    def test_help(self):
        with self.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            for use_commands_service in [True, False]:
                with MockEpoServer(dxl_client,
                                   use_commands_service=use_commands_service):
                    epo_client = EpoClient(
                        dxl_client,
                        epo_unique_id=LOCAL_TEST_SERVER_NAME + str(
                            DEFAULT_EPO_SERVER_ID)
                    )

                    # Run it twice to validate the command vs. remote
                    # service failover logic for request topics
                    for _ in range(2):
                        result = epo_client.help()

                        self.assertEqual(result, HELP_CMD_RESPONSE_PAYLOAD)

    def test_run_command(self):
        with self.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            for use_commands_service in [True, False]:
                with MockEpoServer(dxl_client,
                                   use_commands_service=use_commands_service):
                    epo_client = EpoClient(
                        dxl_client,
                        epo_unique_id=LOCAL_TEST_SERVER_NAME + str(
                            DEFAULT_EPO_SERVER_ID)
                    )

                    # Run it twice to validate the command vs. remote
                    # service failover logic for request topics
                    for _ in range(2):
                        res = epo_client.run_command(
                            "system.find",
                            {"searchText": SYSTEM_FIND_OSTYPE_LINUX},
                            output_format=OutputFormat.JSON
                        )

                        res_list = MessageUtils.json_to_dict(res)

                        self.assertEqual(res_list, SYSTEM_FIND_PAYLOAD)
