Basic System Find Example
=========================

This sample invokes and displays the results of a "system find" remote command via the ePO DXL service.
The results of the find command are displayed in JSON format.

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* An ePO DXL service is running and available on the fabric. If version 5.0
  or later of the DXL ePO extensions are installed on your ePO server, an
  ePO DXL service should already be running on the fabric. If you are using an
  earlier version of the DXL ePO extensions, you can use the
  `ePO DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`_.
* The client is authorized to invoke the ePO DXL Service, and the user that is
  connecting to the ePO server (within the ePO DXL service) has permission to
  execute the "system find" remote command (see :doc:`authorization`).

Setup
*****

Modify the example to include the `unique identifier` associated with the ePO to invoke the remote command on.

For more information on the ePO unique identifier, refer to the following:

* `Configuration File for ePO DXL Python Service (uniqueId property) <https://opendxl.github.io/opendxl-epo-service-python/pydoc/configuration.html#dxl-service-configuration-file-dxleposervice-config>`_
*  The :func:`dxlepoclient.client.EpoClient.lookup_epo_unique_identifiers` method which will return a ``set``
   containing the identifiers for all ePO servers that are currently connected to the fabric.

For example:

    .. code-block:: python

        EPO_UNIQUE_ID = "epo1"

If only one ePO server is connected to the DXL fabric this constant can be set to ``None`` (the client will
automatically determine the ePO's unique identifier).

Modify the example to include the search text for the system find command.

For example:

    .. code-block:: python

        SEARCH_TEXT = "broker"


Running
*******

To run this sample execute the ``sample/basic/basic_system_find_example.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_system_find_example.py

The output should appear similar to the following:

    .. code-block:: python

        [
            {
                "EPOBranchNode.AutoID": 7,
                "EPOComputerProperties.CPUSerialNum": "N/A",
                "EPOComputerProperties.CPUSpeed": 2794,
                "EPOComputerProperties.CPUType": "Intel(R) Core(TM) i7-4980HQ CPU @ 2.80GHz",
                "EPOComputerProperties.ComputerName": "broker1",
                "EPOComputerProperties.DefaultLangID": "0409",
                "EPOComputerProperties.Description": null,

                ...
            }
        ]

The properties for each system found will be displayed.

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # The ePO unique identifier
        EPO_UNIQUE_ID = None

        # The search text
        SEARCH_TEXT = "broker"

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            # Create the ePO client
            epo_client = EpoClient(client, EPO_UNIQUE_ID)

            # Run the system find command
            res = epo_client.run_command("system.find", {"searchText": SEARCH_TEXT})

            # Load find result into list
            res_list = MessageUtils.json_to_dict(res)

            # Display the results
            print(MessageUtils.dict_to_json(res_list, pretty_print=True))


Once a connection is established to the DXL fabric, a :class:`dxlepoclient.client.EpoClient` instance is created
which will be used to invoke remote commands on the ePO server. The `unique identifier` of the ePO server
to invoke remote commands on is specified as an argument to the client constructor. In this particular case, a
value of ``None`` is specified which triggers the client to automatically determine the ePO server's unique identifier.
This will not work if multiple ePO servers are connected to the fabric (an exception will be raised).

Next, the :func:`dxlepoclient.client.EpoClient.run_command` method is invoked
with a ``searchText`` parameter that is specified with the value of ``broker``.

Finally, the JSON response text is loaded into a Python ``list``, formatted,
and displayed to the screen.
