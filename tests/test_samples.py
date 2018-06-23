import json
import os
import threading
import subprocess

from tests.test_base import BaseEpoClientTest
from tests.test_value_constants import *
from tests.mock_eposerver import MockEpoServer

SAMPLE_FOLDER = str(os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
).replace("\\", "/")) + "/sample"

BASIC_FOLDER = SAMPLE_FOLDER + "/basic"

COMMON_PY_FILENAME = SAMPLE_FOLDER + "/common.py"
NEW_COMMON_PY_FILENAME = COMMON_PY_FILENAME + ".new"

CONFIG_FOLDER = str(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"))
CONFIG_FILENAME = CONFIG_FOLDER + "/dxlclient.config"
NEW_CONFIG_FILENAME = CONFIG_FILENAME + ".new"
CA_FILENAME = CONFIG_FOLDER + "/ca-bundle.crt"
CERT_FILENAME = CONFIG_FOLDER + "/client.crt"
KEY_FILENAME = CONFIG_FOLDER + "/client.key"

def overwrite_file_line(filename, target, replacement):
    base_file = open(filename, 'r')
    new_file = open(filename + ".new", "w+")

    for line in base_file:
        if line.startswith(target):
            line = replacement
        new_file.write(line)

    base_file.close()
    new_file.close()

    os.remove(filename)
    os.rename(filename + ".new", filename)


def overwrite_common_py():
    target_line = "CONFIG_FILE = "
    replacement_line = target_line + "\"" + CONFIG_FILENAME + "\"\n"
    overwrite_file_line(COMMON_PY_FILENAME, target_line, replacement_line)


def overwrite_config_cert_locations():
    target_line = "BrokerCertChain = "
    replacement_line = target_line + "\"" + CA_FILENAME + "\"\n"
    overwrite_file_line(CONFIG_FILENAME, target_line, replacement_line)

    target_line = "CertFile = "
    replacement_line = target_line + "\"" + CERT_FILENAME + "\"\n"
    overwrite_file_line(CONFIG_FILENAME, target_line, replacement_line)

    target_line = "PrivateKey = "
    replacement_line = target_line + "\"" + KEY_FILENAME + "\"\n"
    overwrite_file_line(CONFIG_FILENAME, target_line, replacement_line)

class SampleRunner(object):

    def __init__(self, cmd, target=''):
        self.cmd = cmd
        self.target_file = target
        self.process = None
        self.output = "Not started"


    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(
                [self.cmd, self.target_file],
                stdout=subprocess.PIPE,
                #stderr=subprocess.PIPE,
            )
            self.output = self.process.communicate()[0]

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()

        return self.output.decode('utf-8')

class TestCoreHelpSample(BaseEpoClientTest):

    def test_corehelp_example(self):
        # Modify common/config files to work with local ".\test" directory
        overwrite_common_py()
        overwrite_config_cert_locations()

        # Modify sample file to include necessary sample data
        sample_filename = BASIC_FOLDER + "/basic_core_help_example.py"

        target_line = "EPO_UNIQUE_ID = "
        replacement_line = target_line + "\"" \
                           + LOCAL_TEST_SERVER_NAME \
                           + str(DEFAULT_EPO_SERVER_ID) \
                           + "\"\n"
        overwrite_file_line(sample_filename, target_line, replacement_line)

        with self.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            mock_epo_server = MockEpoServer(dxl_client, id_number=DEFAULT_EPO_SERVER_ID)
            dxl_client.connect()
            mock_epo_server.start_service()

            sample_runner = SampleRunner(
                cmd="python",
                target=sample_filename
            )
            output = sample_runner.run(timeout=10)

            self.assertNotIn("Error", str(output))
            self.assertIn(
                HELP_CMD_RESPONSE_PAYLOAD,
                output.replace('\r', '')
            )

            mock_epo_server.stop_service()
            dxl_client.disconnect()


class TestSystemFindSample(BaseEpoClientTest):

    def test_systemfind_example(self):
        # Modify common/config files to work with local ".\test" directory
        overwrite_common_py()
        overwrite_config_cert_locations()

        # Modify sample file to include necessary sample data
        sample_filename = BASIC_FOLDER + "/basic_system_find_example.py"

        target_line = "EPO_UNIQUE_ID = "
        replacement_line = target_line + "\"" \
                           + LOCAL_TEST_SERVER_NAME \
                           + str(DEFAULT_EPO_SERVER_ID) \
                           + "\"\n"
        overwrite_file_line(sample_filename, target_line, replacement_line)

        target_line = "SEARCH_TEXT = "
        replacement_line = target_line + "\"" + SYSTEM_FIND_OSTYPE_LINUX + "\"\n"
        overwrite_file_line(sample_filename, target_line, replacement_line)

        with self.create_client(max_retries=0) as dxl_client:
            # Set up client, and register mock service
            mock_epo_server = MockEpoServer(dxl_client, id_number=DEFAULT_EPO_SERVER_ID)
            dxl_client.connect()
            mock_epo_server.start_service()

            sample_runner = SampleRunner(
                cmd="python",
                target=sample_filename
            )
            output = sample_runner.run(timeout=10)

            self.assertNotIn("Error", output)
            self.assertListEqual(
                SYSTEM_FIND_PAYLOAD,
                json.loads(''.join(output))
            )

            mock_epo_server.stop_service()
            dxl_client.disconnect()
