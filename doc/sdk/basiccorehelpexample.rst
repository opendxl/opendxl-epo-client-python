Basic Core Help Example
========================

This sample invokes and displays the results of the "core help" remote command via the ePO DXL service.
The "core help" command lists the remote commands that are exposed by a particular ePO server.


Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The ePO DXL service is running and available on the fabric (see `ePO DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`_)
* The client is authorized to invoke the ePO DXL Service (see `ePO DXL Service Client Authorization <https://opendxl.github.io/opendxl-epo-service-python/pydoc/authorization.html#client-authorization>`_)

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

Running
*******

To run this sample execute the ``sample/basic/basic_core_help_example.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_core_help_example.py

The output should appear similar to the following:

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
        ComputerMgmt.deleteTagGroup tagGroupIds [deleteTags] - Delete one or more Tag
        Groups.
        ComputerMgmt.listAllTagGroups - List All Tag Groups in Tag Group Tree
        ComputerMgmt.moveTagsToTagGroup tagIds tagGroupId - Move tags to an existing tag
        group.

        ...

Each remote command exposed by the particular ePO server is listed along with its associated parameters.

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # The ePO unique identifier
        EPO_UNIQUE_ID = None

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            # Create the ePO client
            epo_client = EpoClient(client, EPO_UNIQUE_ID)

            # Display the help
            print(epo_client.help())


Once a connection is established to the DXL fabric, a :class:`dxlepoclient.client.EpoClient` instance is created
which will be used to invoke remote commands on the ePO server. The `unique identifier` of the ePO server
to invoke remote commands on is specified as an argument to the client constructor. In this particular case, a
value of ``None`` is specified which triggers the client to automatically determine the ePO server's unique identifier.
This will not work if multiple ePO servers are connected to the fabric (an exception will be raised).

Next, the results of invoking the :func:`dxlepoclient.client.EpoClient.help` method are displayed to the screen.
