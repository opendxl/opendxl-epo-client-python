import json
import os
import re
import sys

from tempfile import NamedTemporaryFile
from mock import patch
from tests.test_base import BaseClientTest
from tests.test_value_constants import *
from tests.mock_eposerver import MockEpoServer

if sys.version_info[0] > 2:
    import builtins  # pylint: disable=import-error, unused-import
else:
    import __builtin__  # pylint: disable=import-error

    builtins = __builtin__  # pylint: disable=invalid-name


def expected_print_output(detail):
    json_string = json.dumps(
        detail,
        sort_keys=True,
        separators=(".*", ": ")
    )

    return re.sub(
        r"(\.\*)+",
        ".*",
        re.sub(
            r"[{[\]}]",
            ".*",
            json_string
        )
    )


class StringContains(object):
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, other):
        return self.pattern in other


class StringDoesNotContain(object):
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, other):
        return not self.pattern in other


class StringMatchesRegEx(object):
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, other):
        return re.match(self.pattern, other, re.DOTALL)


class StringDoesNotMatchRegEx(object):
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, other):
        return not re.match(self.pattern, other)


def run_sample(sample_file):
    with open(sample_file) as f, \
            patch.object(builtins, 'print') as mock_print:
        sample_globals = {"__file__": sample_file}
        exec(f.read(), sample_globals)  # pylint: disable=exec-used
    return mock_print


class TempSampleFile(object):

    @property
    def temp_file(self):
        return self._temp_file

    def __init__(self, sample_filename):
        self._temp_file = NamedTemporaryFile(
            mode="w+",
            dir=os.path.dirname(sample_filename),
            delete=False)
        self._temp_file.close()
        os.chmod(self._temp_file.name, 0o777)
        self.base_filename = sample_filename
        self.write_file_line()

    def write_file_line(self, target=None, replacement=None):
        with open(self.base_filename, 'r') as base_file:
            with open(self._temp_file.name, 'w+') as new_sample_file:

                for line in base_file:
                    if target != None and replacement != None:
                        if line.startswith(target):
                            line = replacement
                    new_sample_file.write(line)


    def __del__(self):
        self.temp_file.close()
        os.remove(self._temp_file.name)


class TestSamples(BaseClientTest):

    SAMPLE_FOLDER = str(
        os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
    )+ "/sample"

    BASIC_FOLDER = SAMPLE_FOLDER + "/basic"

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
                mock_print = run_sample(temp_sample_file.temp_file.name)

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
                mock_print = run_sample(temp_sample_file.temp_file.name)

                mock_print.assert_any_call(
                    StringMatchesRegEx(
                        expected_print_output(SYSTEM_FIND_PAYLOAD)
                    )
                )

                mock_print.assert_any_call(
                    StringDoesNotContain("Error")
                )

            dxl_client.disconnect()
