# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2017 McAfee Inc. - All Rights Reserved.
################################################################################

from __future__ import absolute_import
import logging
import os
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

    # The type of the ePO DXL "remote" service that is registered with
    # the fabric
    DXL_SERVICE_TYPE = "/mcafee/service/epo/remote"
    _DXL_EPO_REMOTE_SERVICE_TYPE = DXL_SERVICE_TYPE

    # The prefix for ePO DXL "remote" service request topics
    DXL_REQUEST_PREFIX = DXL_SERVICE_TYPE + "/"
    _DXL_EPO_REMOTE_REQUEST_PREFIX = DXL_REQUEST_PREFIX

    # The format for request topics that are associated with the ePO DXL
    # "remote" service
    DXL_REQUEST_FORMAT = DXL_REQUEST_PREFIX + "{0}"
    _DXL_EPO_REMOTE_REQUEST_FORMAT = DXL_REQUEST_FORMAT

    # The default amount of time (in seconds) to wait for a response from the ePO DXL service
    DEFAULT_RESPONSE_TIMEOUT = Client._DEFAULT_RESPONSE_TIMEOUT

    # The minimum amount of time (in seconds) to wait for a response from the ePO DXL service
    MIN_RESPONSE_TIMEOUT = Client._MIN_RESPONSE_TIMEOUT

    # The type of the ePO DXL "commands" service that is registered with
    # the fabric
    _DXL_EPO_COMMANDS_SERVICE_TYPE = "/mcafee/service/epo/commands"

    # The format for request topics that are associated with the ePO DXL
    # "commands" service
    _DXL_EPO_COMMANDS_REQUEST_FORMAT = \
        "/mcafee/service/epo/command/{0}/remote/{1}"

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
        :raise Exception: If a value is provided for `epo_unique_id` but
            no matching service is registered with the DXL fabric.
        """
        super(EpoClient, self).__init__(dxl_client)
        self._dxl_client = dxl_client

        # Need to be connected to the DXL fabric before making any service
        # registry queries
        if not dxl_client.connected:
            dxl_client.connect()

        # Controls whether the built-in ePO "commands" (True) or
        # standalone "remote" service
        # (https://github.com/opendxl/opendxl-epo-service-python)
        # (False) is used to make command requests
        self._use_epo_commands_service = True

        if epo_unique_id:
            logger.debug("Validating the ePO service identifier...")
            self._use_epo_commands_service = \
                self._is_epo_unique_id_for_commands_service(
                    epo_unique_id, self._dxl_client, self._response_timeout)
        else:
            logger.debug("Attempting to find ePO service identifier...")
            self._use_epo_commands_service, epo_ids = \
                self._lookup_epo_unique_identifiers(self._dxl_client,
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
                        ", ".join(sorted(epo_ids))))

        self._epo_unique_id = epo_unique_id

    def run_command(self, command_name, params=None,
                    output_format=OutputFormat.JSON):
        """
        Invokes an ePO remote command on the ePO server this client is communicating with.

        **Example Usage**

            .. code-block:: python

                # Run the system find command
                result = epo_client.run_command("system.find",
                                                {"searchText": "mySystem"})

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
            returning the response. The list of `output formats` can be found
            in the :class:`OutputFormat` constants class. This parameter can
            only be set to a value other than :const:`OutputFormat.JSON`
            when the command is processed by a
            `McAfee ePO DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`_
            service. If the command is processed by the ePO-hosted
            `DXL commands` service, this parameter can only be set to
            :const:`OutputFormat.JSON`. For compatibility across ePO service
            configurations, it is suggested to not set this parameter (using
            the default value of :const:`OutputFormat.JSON`).
        :raise Exception: If an unsupported `output format` is specified. This
            exception is raised if the command is to be sent to an ePO-hosted
            `DXL Commands` service and an `output format` of anything other
            than :const:`OutputFormat.JSON` is specified.
        :return: The result of the remote command execution
        """
        OutputFormat.validate(output_format)
        if params is None:
            params = {}

        # Try the request through the `commands` service first. If that fails
        # due to the service not being found, try the request again through
        # the `remote` service. Update the `_use_epo_commands_service`
        # variable based on which service the request could be made through
        # so that subsequent requests can be made through the valid service.
        # Non-JSON requests are attempted through the `remote` service first
        # since the `commands` service only supports JSON.
        if self._use_epo_commands_service and \
                output_format == OutputFormat.JSON:
            res = self._invoke_epo_commands_service(
                command_name, output_format, params)
        else:
            res = self._invoke_epo_remote_service(
                command_name, output_format, params
            )

        return self._decode_response(res)

    def help(self, output_format=OutputFormat.VERBOSE):
        # pylint: disable=line-too-long
        """
        Returns the list of remote commands that are supported by the ePO server this client is
        communicating with.

        **Example Usage**

            .. code-block:: python

                # Display the help
                print(epo_client.help())

        **Example Response**

            .. parsed-literal::

                ComputerMgmt.createAgentDeploymentUrlCmd deployPath groupId urlName
                agentVersionNumber agentHotFix [edit] [ahId] [fallBackAhId] - Create Agent
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
            returning the response. The list of `output formats` can be found
            in the :class:`OutputFormat` constants class. If the command is
            processed by the ePO-hosted `DXL Commands` service, this parameter
            can only be set to :const:`OutputFormat.VERBOSE` or
            :const:`OutputFormat.JSON`.
        :raise Exception: If an unsupported `output format` is specified. This
            exception is raised if the command is to be sent to an ePO-hosted
            `DXL Commands` service and an `output format` of anything other
            than :const:`OutputFormat.VERBOSE` or :const:`OutputFormat.JSON`
            is specified.
        :return: The result of the remote command execution
        """
        res = self.run_command(
            "core.help",
            output_format=OutputFormat.JSON \
                if output_format == OutputFormat.VERBOSE else output_format)
        if output_format == OutputFormat.VERBOSE:
            res_list = MessageUtils.json_to_dict(res)
            res = os.linesep.join(res_list)
        return res

    def _invoke_epo_commands_service(self, command_name,
                                     output_format, params):
        """
        Invokes the ePO DXL "commands" service for the purposes of executing a
        remote command.

        :param command_name: The name of the remote command to invoke
        :param output_format: The output format for ePO to use when returning
            the response
        :param params: A dictionary (``dict``) containing the parameters for
            the command
        :return: A DXL Response object containing the result of the remote
            command execution
        """
        if output_format != OutputFormat.JSON:
            raise Exception(
                "Invalid output format: " + output_format +
                ". ePO commands service only supports " +
                OutputFormat.JSON + ".")

        return self._invoke_epo_service(
            self._DXL_EPO_COMMANDS_REQUEST_FORMAT.format(
                self._epo_unique_id,
                command_name.replace(".", "/")
            ),
            params
        )

    def _invoke_epo_remote_service(self, command_name, output_format, params):
        """
        Invokes the ePO DXL "remote" service for the purposes of executing a
        remote command.

        :param command_name: The name of the remote command to invoke
        :param output_format: The output format for ePO to use when returning
            the response
        :param params: A dictionary (``dict``) containing the parameters for
            the command
        :return: A DXL Response object containing the result of the remote
            command execution
        """
        return self._invoke_epo_service(
            self._DXL_EPO_REMOTE_REQUEST_FORMAT.format(self._epo_unique_id),
            {
                "command": command_name,
                "output": output_format,
                "params": params
            }
        )

    def _invoke_epo_service(self, request_topic, payload_dict):
        """
        Invokes the ePO DXL service for the purposes of executing a remote
        command.

        :param request_topic: DXL request topic to use for the request
        :param payload_dict: The dictionary (``dict``) to use as the payload
          of the DXL request
        :return: A DXL Response object containing the result of the remote
            command execution
        """
        return self._sync_request(
            self._dxl_client,
            Request(request_topic),
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
                     MessageUtils.dict_to_json(payload_dict,
                                               pretty_print=True))

        # Send the request and wait for a response (synchronous)
        return dxl_client.sync_request(request, timeout=response_timeout)

    @staticmethod
    def _decode_response(res):
        """
        Decodes the payload from DXL Response object into a string.

        :param res: The DXL Response object to decode.
        :return: The decoded payload.
        :raise Exception: If ``res`` is an ErrorResponse.
        """
        if res.message_type == Message.MESSAGE_TYPE_ERROR:
            raise Exception("Error: " + res.error_message + " (" + str(
                res.error_code) + ")")

        # Return a dictionary corresponding to the response payload
        ret_val = MessageUtils.decode_payload(res)

        # Display the response
        logger.debug("Response:\n%s", ret_val)
        return ret_val

    @staticmethod
    def _query_service_registry(dxl_client, response_timeout, service_type):
        """
        Queries the broker service registry for services.

        :param dxl_client: The DXL client with which to perform the request.
        :param response_timeout: The maximum amount of time to wait for a
            response.
        :param service_type: The service type to return data for.
        :return: A ``list`` containing info for each registered service whose
            ``service_type`` matches the ``service_type`` parameter passed
            into this method.
        """
        res = EpoClient._decode_response(
            EpoClient._sync_request(
                dxl_client,
                Request("/mcafee/service/dxl/svcregistry/query"),
                response_timeout,
                {"serviceType": service_type}))
        res_dict = MessageUtils.json_to_dict(res)
        return res_dict["services"].values() if "services" in res_dict else []

    @staticmethod
    def _lookup_epo_commands_service_unique_ids(dxl_client, response_timeout):
        """
        Returns a ``set`` containing the unique identifiers for the ePO servers
        that are currently exposed to the DXL fabric via an ePO "commands"
        service. "commands" services are registered by version 5.0 and
        later of the ePO DXL extensions.

        :param dxl_client: The DXL client with which to perform the request.
        :param response_timeout: The maximum amount of time to wait for a
            response.
        :return: A ``set`` containing the unique identifiers for the ePO
            servers that are currently exposed to the DXL fabric.
        """
        services = EpoClient._query_service_registry(
            dxl_client, response_timeout,
            EpoClient._DXL_EPO_COMMANDS_SERVICE_TYPE)
        ret_ids = set()
        for service in services:
            if "metaData" in service:
                metadata = service["metaData"]
                if "epoGuid" in metadata:
                    ret_ids.add(metadata["epoGuid"])
        return ret_ids

    @staticmethod
    def _lookup_epo_remote_service_unique_ids(dxl_client, response_timeout):
        """
        Returns a ``set`` containing the unique identifiers for the ePO servers
        that are currently exposed to the DXL fabric via an ePO "remote"
        service. "remote" services are registered by the standalone
        `ePO DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`__.

        :param dxl_client: The DXL client with which to perform the request.
        :param response_timeout: The maximum amount of time to wait for a
            response.
        :return: A ``set`` containing the unique identifiers for the ePO
            servers that are currently exposed to the DXL fabric.
        """
        services = EpoClient._query_service_registry(
            dxl_client, response_timeout,
            EpoClient.DXL_SERVICE_TYPE)
        ret_ids = set()
        for service in services:
            if "requestChannels" in service:
                for channel in service["requestChannels"]:
                    if channel.startswith(
                            EpoClient._DXL_EPO_REMOTE_REQUEST_PREFIX):
                        ret_ids.add(
                            channel[len(
                                EpoClient._DXL_EPO_REMOTE_REQUEST_PREFIX):]
                        )
        return ret_ids

    @staticmethod
    def _is_epo_unique_id_for_commands_service(
            epo_unique_id, dxl_client,
            response_timeout=Client._DEFAULT_RESPONSE_TIMEOUT):
        """
        Determines if the supplied ``epoUniqueId`` maps to a ePO DXL
        "commands" or a "remote" service.

        :param epo_unique_id: The unique identifier used to specify
            the ePO server that this client will communicate with.
        :param dxl_client: The DXL client to use for communication with the ePO
            DXL service
        :param response_timeout: (optional) The maximum amount of time to wait
            for a response
        :return: ``True`` if the unique identifier matches a "commands"
            service, ``False`` if the unique identifier matches a "remote"
            service.
        :raise Exception: If no service matching the unique id is registered
            with the DXL fabric.
        """
        id_for_commands_service = False
        if epo_unique_id not in \
                EpoClient._lookup_epo_remote_service_unique_ids(
                        dxl_client, response_timeout):
            if epo_unique_id in \
                    EpoClient._lookup_epo_commands_service_unique_ids(
                            dxl_client, response_timeout):
                id_for_commands_service = True
            else:
                raise Exception("No ePO DXL services are registered with " +
                                "the DXL fabric for id: " + epo_unique_id)
        return id_for_commands_service

    @staticmethod
    def _lookup_epo_unique_identifiers(dxl_client, response_timeout):
        """
        Returns a ``tuple`` where the first item is a ``bool`` representing
        whether the returned ids are for "commands" services (``True``) or
        "remote" services (``False``) and the second item is a ``set``
        containing the unique identifiers for the ePO servers that are
        currently exposed to the DXL fabric.

        :param dxl_client: The DXL client with which to perform the request
        :param response_timeout: (optional) The maximum amount of time to wait
            for a response
        :return: A ``tuple`` where the first item is a ``bool`` representing
            whether a "commands" service (``True``) or "remote" service
            (``False``) should be used. If at least one "remote" service is
            available, a "remote" service should be used. The second item in
            the ``tuple`` is a ``set`` containing the unique identifiers for
            the ePO servers that are currently exposed to the DXL fabric.
        """
        epo_remote_service_ids = \
            EpoClient._lookup_epo_remote_service_unique_ids(dxl_client,
                                                            response_timeout)
        epo_command_service_ids = \
            EpoClient._lookup_epo_commands_service_unique_ids(dxl_client,
                                                              response_timeout)
        return not epo_remote_service_ids, \
            epo_command_service_ids.union(epo_remote_service_ids)

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
        return EpoClient._lookup_epo_unique_identifiers(
            dxl_client, response_timeout)[1]
