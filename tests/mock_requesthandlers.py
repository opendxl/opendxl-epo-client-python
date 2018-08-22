import json

from dxlbootstrap.util import MessageUtils
from dxlclient.callbacks import RequestCallback
from dxlclient.message import Response, ErrorResponse
from tests.test_value_constants import *


class FakeEpoServerCallback(RequestCallback):
    # The format for request topics that are associated with the ePO DXL
    # "remote" service. "remote" services are registered by the standalone ePO
    # DXL Python service
    # (https://github.com/opendxl/opendxl-epo-service-python).
    EPO_REMOTE_REQUEST_TOPIC = "/mcafee/service/epo/remote/" + \
                               LOCAL_TEST_SERVER_NAME + "{}"

    # The format for request topics that are associated with the ePO DXL
    # "commands" service. "commands" services are registered by version 5.0 and
    # later of the DXL Broker Management extension in ePO.
    EPO_COMMAND_REQUEST_TOPIC = "/mcafee/service/epo/command/" + \
        LOCAL_TEST_SERVER_NAME + "{}/remote/#"

    TEST_SYSTEM_NAME = "sys1"

    # UTF-8 encoding (used for encoding/decoding payloads)
    UTF_8 = "utf-8"

    # The key in the request used to specify the ePO command to invoke
    CMD_NAME_KEY = "command"
    # The key in the request used to specify the output format
    # (json, xml, verbose, terse). This is optional
    OUTPUT_KEY = "output"
    # The key used to specify the parameters for the ePO command
    PARAMS_KEY = "params"

    # The default output format
    DEFAULT_OUTPUT = "json"

    KNOWN_COMMANDS = [
        {
            "name": "core.help",
            "parameters": [
                "command",
                "prefix=<>"
            ],
            "description": "Displays a list of all commands and help \r\nstrings."
        },
        {
            "name": "system.find",
            "parameters": [
                "searchText",
                "searchNameOnly"
            ],
            "description": "Finds systems in the System Tree"
        }
    ]

    @property
    def epo_request_topic(self):
        request_topic = self.EPO_COMMAND_REQUEST_TOPIC \
            if self.use_commands_service else self.EPO_REMOTE_REQUEST_TOPIC
        return request_topic.format(self.id_number)

    def __init__(self, client, id_number, use_commands_service,
                 user_authorized):
        super(FakeEpoServerCallback, self).__init__()

        self._client = client
        self.id_number = str(id_number)
        self.use_commands_service = use_commands_service
        self.user_authorized = user_authorized

    def on_request(self, request):
        try:
            if not self.user_authorized:
                return

            # Build dictionary from the request payload
            req_dict = json.loads(request.payload.decode(encoding=self.UTF_8))

            if self.use_commands_service:
                # Determine the ePO command
                command = request.destination_topic[
                    len(self.epo_request_topic)-1:].replace("/", ".")

                # Determine the command parameters
                params = req_dict
            else:
                # Determine the ePO command
                if self.CMD_NAME_KEY not in req_dict:
                    raise Exception(
                        "A command name was not specified ('{0}')".format(
                            self.CMD_NAME_KEY))
                command = req_dict[self.CMD_NAME_KEY]

                # Determine the command parameters
                params = req_dict[self.PARAMS_KEY]

            # Help command received
            if command == CORE_HELP_CMD_NAME:
                self.help_command(request)

            # System Find command
            elif command == SYSTEM_FIND_CMD_NAME:
                self.system_find_command(request, params)

            # Unknown Command
            else:
                self.unknown_command(request, command)

        except Exception as ex:
            # Send error response
            self._client.send_response(
                ErrorResponse(request,
                              error_message=str(ex).encode(
                                  encoding=self.UTF_8)))

    def help_command(self, request):
        # Create the response
        response = Response(request)

        cmd_array = []
        for cmd in self.KNOWN_COMMANDS:

            cmd_string = cmd["name"] + " "

            for param in cmd["parameters"]:
                cmd_string += "[" + param + "] "

            cmd_string += "- " + cmd["description"]

            cmd_array.append(cmd_string)

        response.payload = MessageUtils.dict_to_json(cmd_array)

        self._client.send_response(response)

    def system_find_command(self, request, params):
        # Create the response
        response = Response(request)

        response.payload = MessageUtils.dict_to_json(
            SYSTEM_FIND_PAYLOAD
            if params == {"searchText": SYSTEM_FIND_OSTYPE_LINUX}
            else [])

        self._client.send_response(response)

    def unknown_command(self, request, command):
        # Create the response
        response = Response(request)

        response.payload = ERROR_RESPONSE_PAYLOAD_PREFIX + command

        self._client.send_response(response)
