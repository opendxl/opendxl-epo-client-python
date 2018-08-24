import os

LOCAL_TEST_SERVER_NAME = "local_test"
DEFAULT_EPO_SERVER_ID = 0

ERROR_RESPONSE_PAYLOAD_PREFIX = "Error 1 : \nNo such command: "

CORE_HELP_CMD_NAME = "core.help"

HELP_CMD_RESPONSE_PAYLOAD = os.linesep.join([
    "core.help [command] [prefix=<>] - Displays a list of all commands and help \r\nstrings.",
    "system.find [searchText] [searchNameOnly] - Finds systems in the System Tree"
])

SYSTEM_FIND_CMD_NAME = "system.find"

SYSTEM_FIND_OSTYPE_LINUX = "Linux"

SYSTEM_FIND_PAYLOAD = [
    {
        "EPOBranchNode.AutoID": 4,
        "EPOComputerProperties.OSType": SYSTEM_FIND_OSTYPE_LINUX,
        "EPOComputerProperties.OSVersion": "4.9",
        "EPOComputerProperties.Vdi": 0,
        "EPOLeafNode.AgentGUID": "11111111-2222-3333-4444-555555555555",
        "EPOLeafNode.ManagedState": 1,
        "EPOLeafNode.Tags": "DXLBROKER, Server"
    },
    {
        "EPOBranchNode.AutoID": 4,
        "EPOComputerProperties.OSType": SYSTEM_FIND_OSTYPE_LINUX,
        "EPOComputerProperties.OSVersion": "4.9",
        "EPOComputerProperties.Vdi": 0,
        "EPOLeafNode.AgentGUID": "66666666-7777-8888-9999-000000000000",
        "EPOLeafNode.ManagedState": 1,
        "EPOLeafNode.Tags": "DXLBROKER, Server"
    }
]
