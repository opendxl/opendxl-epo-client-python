from tests.test_base import *
from tests.test_value_constants import *
from tests.mock_eposerver import MockEpoServer


class TestSamples(BaseClientTest):

    def test_corehelp_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_core_help_example.py"
        temp_sample_file = TempSampleFile(sample_filename)

        target_line = "EPO_UNIQUE_ID = "
        replacement_line = target_line + "\"" \
                           + LOCAL_TEST_SERVER_NAME \
                           + str(DEFAULT_EPO_SERVER_ID) \
                           + "\"\n"
        temp_sample_file.write_file_line(target_line, replacement_line)

        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockEpoServer(dxl_client, id_number=DEFAULT_EPO_SERVER_ID):
                mock_print = BaseClientTest.run_sample(temp_sample_file.temp_file.name)

                mock_print.assert_any_call(
                    StringContains(HELP_CMD_RESPONSE_PAYLOAD)
                )

                mock_print.assert_any_call(
                    StringDoesNotContain("Error")
                )

            dxl_client.disconnect()

    def test_systemfind_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_system_find_example.py"
        temp_sample_file = TempSampleFile(sample_filename)

        target_line = "EPO_UNIQUE_ID = "
        replacement_line = target_line + "\"" \
                           + LOCAL_TEST_SERVER_NAME \
                           + str(DEFAULT_EPO_SERVER_ID) \
                           + "\"\n"
        temp_sample_file.write_file_line(target_line, replacement_line)

        target_line = "SEARCH_TEXT = "
        replacement_line = target_line + "\"" + SYSTEM_FIND_OSTYPE_LINUX + "\"\n"
        temp_sample_file.write_file_line(target_line, replacement_line)

        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockEpoServer(dxl_client, id_number=DEFAULT_EPO_SERVER_ID):
                mock_print = BaseClientTest.run_sample(temp_sample_file.temp_file.name)

                mock_print.assert_any_call(
                    StringMatchesRegEx(
                        BaseClientTest.expected_print_output(SYSTEM_FIND_PAYLOAD)
                    )
                )

                mock_print.assert_any_call(
                    StringDoesNotContain("Error")
                )

            dxl_client.disconnect()
