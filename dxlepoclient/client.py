# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2017 McAfee Inc. - All Rights Reserved.
################################################################################

from __future__ import absolute_import
import logging
from dxlclient import Request, Message
from dxlbootstrap.client import Client
from dxlbootstrap.util import MessageUtils

# Configure local logger
logger = logging.getLogger(__name__)


class OutputFormat(object):
    """
    Constants that are used to indicate the `output format` for ePO to use when responding to a
    remote command invocation.

        +---------+-------------------------------------------------------+
        | Type    | Description                                           |
        +=========+=======================================================+
        | JSON    | JSON format                                           |
        +---------+-------------------------------------------------------+
        | XML     | XML format                                            |
        +---------+-------------------------------------------------------+
        | VERBOSE | Text-based format (verbose)                           |
        +---------+-------------------------------------------------------+
        | TERSE   | Text-based format (terse)                             |
        +---------+-------------------------------------------------------+
    """
    JSON = "json"
    XML = "xml"
    VERBOSE = "verbose"
    TERSE = "terse"

    @staticmethod
    def validate(output_format):
        """
        Validates that the specified format is valid (json, xml, etc.). If the format is not valid
        an exception is thrown.

        :param output_format: The output format
        """
        if output_format not in [OutputFormat.JSON, OutputFormat.XML,
                                 OutputFormat.VERBOSE, OutputFormat.TERSE]:
            raise Exception("Invalid output format: {0}".format(output_format))


class EpoClient(Client):
    """
    This client provides a high level wrapper for invoking ePO remote commands
    via the Data Exchange Layer (DXL) fabric.

    The purpose of this library is to allow users to invoke ePO remote commands
    without having to focus on lower-level details such as ePO-specific DXL
    topics and message formats.
    """

    # The type of the ePO DXL service that is registered with the fabric
    DXL_SERVICE_TYPE = "/mcafee/service/epo/remote"

    # The prefix for ePO DXL service request topics
    DXL_REQUEST_PREFIX = DXL_SERVICE_TYPE + "/"

    # The format for request topics that are associated with the ePO DXL service
    DXL_REQUEST_FORMAT = DXL_REQUEST_PREFIX + "{0}"

    # The default amount of time (in seconds) to wait for a response from the ePO DXL service
    DEFAULT_RESPONSE_TIMEOUT = Client._DEFAULT_RESPONSE_TIMEOUT

    # The minimum amount of time (in seconds) to wait for a response from the ePO DXL service
    MIN_RESPONSE_TIMEOUT = Client._MIN_RESPONSE_TIMEOUT

    def __init__(self, dxl_client, epo_unique_id=None):
        """

        **ePO Unique Identifier**

            DXL supports communicating with multiple ePO servers on a single DXL
            fabric. However, each instance of this client can only be associated
            with one ePO server (the server it will be invoking remote commands
            on).

            The ePO unique identifier specified must match the identifier that
            was associated with the particular ePO when a corresponding ePO DXL
            service was started.

            If only one ePO server is connected to the DXL fabric this parameter
            is optional (the client will automatically determine the ePO's
            unique identifier).

            The :func:`lookup_epo_unique_identifiers` method can be used to
            determine the unique identifiers for ePO servers that are currently
            exposed to the fabric.

        Constructor parameters:

        :param dxl_client: The DXL client to use for communication with the ePO
            DXL service
        :param epo_unique_id: (optional) The unique identifier used to specify
            the ePO server that this client will communicate with.
        """
        super(EpoClient, self).__init__(dxl_client)
        self._dxl_client = dxl_client

        if epo_unique_id is None:
            logger.debug("Attempting to find ePO service identifier...")
            epo_ids = self.lookup_epo_unique_identifiers(self._dxl_client,
                                                         self._response_timeout)

            epo_ids_len = len(epo_ids)
            if epo_ids_len is 1:
                epo_unique_id = next(iter(epo_ids))
            elif epo_ids_len is 0:
                raise Exception(
                    "No ePO DXL services are registered with the DXL fabric")
            else:
                raise Exception((
                    "Multiple ePO DXL services are registered with the DXL fabric ({0}). "
                    "A specific ePO unique identifier must be specified.").format(
                        ", ".join(epo_ids)))

        self._epo_unique_id = epo_unique_id

    def run_command(self, command_name, params=None,
                    output_format=OutputFormat.JSON):
        """
        Invokes an ePO remote command on the ePO server this client is communicating with.

        **Example Usage**

            .. code-block:: python

                # Run the system find command
                result = epo_client.run_command("system.find",
                                                {"searchText": "mySystem"},
                                                output_format=OutputFormat.JSON)

        **Example Response**

            .. code-block:: python

                [
                    {
                        "EPOBranchNode.AutoID": 7,
                        "EPOComputerProperties.CPUSerialNum": "N/A",
                        "EPOComputerProperties.CPUSpeed": 2794,
                        "EPOComputerProperties.CPUType":
                            "Intel(R) Core(TM) i7-4980HQ CPU @ 2.80GHz",
                        "EPOComputerProperties.ComputerName": "mySystemForTesting",
                        "EPOComputerProperties.DefaultLangID": "0409",

                        ...

                    }
                ]

        :param command_name: The name of the remote command to invoke
        :param params: (optional) A dictionary (``dict``) containing the
            parameters for the command
        :param output_format: (optional) The output format for ePO to use when
            returning the response. The list of `output formats` can be found in
            the :class:`OutputFormat` constants class.
        :return: The result of the remote command execution
        """
        OutputFormat.validate(output_format)
        if params is None:
            params = {}

        return self._invoke_epo_service({
            "command": command_name,
            "output": output_format,
            "params": params
        })

    def help(self, output_format=OutputFormat.VERBOSE):
        """
        Returns the list of remote commands that are supported by the ePO server this client is
        communicating with.

        **Example Usage**

            .. code-block:: python

                # Display the help
                print epo_client.help()

        **Example Response**

            .. code-block:: python

                ComputerMgmt.createAgentDeploymentUrlCmd deployPath groupId [edit] [ahId]
                [fallBackAhId] [urlName] [agentVersionNumber] [agentHotFix] - Create Agent
                Deployment URL Command
                ComputerMgmt.createCustomInstallPackageCmd deployPath [ahId] [fallBackAhId] -
                Create Custom Install Package Command
                ComputerMgmt.createDefaultAgentDeploymentUrlCmd tenantId - Create Default
                Non-Editable Agent Deployment URL Command
                ComputerMgmt.createTagGroup parentTagGroupId newTagGroupName - Create a new
                subgroup under an existing tag group.
                ComputerMgmt.deleteTag tagIds [forceDelete] - Delete one or more tags.

                ...

        :param output_format: (optional) The output format for ePO to use when
            returning the response. The list of `output formats` can be found in
            the :class:`OutputFormat` constants class.
        :return: The result of the remote command execution
        """
        return self.run_command("core.help", output_format=output_format)

    def _invoke_epo_service(self, payload_dict):
        """
        Invokes the ePO DXL service for the purposes of executing a remote command
        :param payload_dict: The dictionary (``dict``) to use as the payload of the DXL request
        :return: The result of the remote command execution
        """
        return self._sync_request(
            self._dxl_client,
            Request(self.DXL_REQUEST_FORMAT.format(self._epo_unique_id)),
            self.response_timeout,
            payload_dict)

    @staticmethod
    def _sync_request(dxl_client, request, response_timeout, payload_dict):
        """
        Performs a synchronous DXL request and returns the payload

        :param dxl_client: The DXL client with which to perform the request
        :param request: The DXL request to send
        :param response_timeout: The maximum amount of time to wait for a response
        :param payload_dict: The dictionary (``dict``) to use as the payload of the DXL request
        :return: The result of the remote command execution (resulting payload)
        """
        # Set the payload
        MessageUtils.dict_to_json_payload(request, payload_dict)

        # Display the request that is going to be sent
        logger.debug("Request:\n%s",
                     MessageUtils.dict_to_json(payload_dict, pretty_print=True))

        # Send the request and wait for a response (synchronous)
        res = dxl_client.sync_request(request, timeout=response_timeout)

        # Return a dictionary corresponding to the response payload
        if res.message_type != Message.MESSAGE_TYPE_ERROR:
            ret_val = MessageUtils.decode_payload(res)
            # Display the response
            logger.debug("Response:\n%s", ret_val)
            return ret_val
        else:
            raise Exception("Error: " + res.error_message + " (" + str(
                res.error_code) + ")")

    @staticmethod
    def lookup_epo_unique_identifiers(
            dxl_client, response_timeout=Client._DEFAULT_RESPONSE_TIMEOUT):
        """
        Returns a ``set`` containing the unique identifiers for the ePO servers that are currently
        exposed to the DXL fabric

        :param dxl_client: The DXL client with which to perform the request
        :param response_timeout: (optional) The maximum amount of time to wait for a response
        :return: A ``set`` containing the unique identifiers for the ePO servers that are currently
            exposed to the DXL fabric.
        """
        res = EpoClient._sync_request(
            dxl_client,
            Request("/mcafee/service/dxl/svcregistry/query"),
            response_timeout,
            {"serviceType": EpoClient.DXL_SERVICE_TYPE})
        res_dict = MessageUtils.json_to_dict(res)

        ret_ids = set()
        if "services" in res_dict:
            for service in res_dict["services"].values():
                if "requestChannels" in service:
                    channels = service['requestChannels']
                    for channel in channels:
                        if channel.startswith(EpoClient.DXL_REQUEST_PREFIX):
                            ret_ids.add(
                                channel[len(EpoClient.DXL_REQUEST_PREFIX):])
        return ret_ids
