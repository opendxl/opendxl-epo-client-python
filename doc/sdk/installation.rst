Library Installation
====================

Prerequisites
*************

* OpenDXL Python Client library installed
    `<https://github.com/opendxl/opendxl-client-python>`_

* The OpenDXL Python Client prerequisites must be satisfied
    `<https://opendxl.github.io/opendxl-client-python/pydoc/installation.html>`_

* McAfee ePolicy Orchestrator (ePO) service is running and available on DXL
  fabric

..

  * If version 5.0 or later of the DXL ePO extensions are installed on your ePO
    server, an ePO DXL service should already be running on the fabric.

..

  * If you are using an earlier version of the DXL ePO extensions, you can use the
    `McAfee ePolicy Orchestrator (ePO) DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`_.

* OpenDXL Python Client has permission to invoke ePO remote commands

..

  * If version 5.0 or later of DXL ePO extensions are installed on your ePO
    server, see the :doc:`authorization` page to ensure that the OpenDXL Python
    client has appropriate authorization to perform ePO remote commands.

..

  * If you are using the standalone
    `ePO DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`_
    to proxy remote commands to the ePO server, follow the steps on the
    `ePO DXL Python Service Authorization <https://opendxl.github.io/opendxl-epo-service-python/pydoc/authorization.html#client-authorization>`_
    page to ensure that the OpenDXL Python client has appropriate authorization
    to perform ePO remote commands.

* Python 2.7.9 or higher in the Python 2.x series or Python 3.4.0 or higher
  in the Python 3.x series installed within a Windows or Linux environment.

Installation
************

Use ``pip`` to automatically install the module:

    .. parsed-literal::

        pip install dxlepoclient-\ |version|\-py2.py3-none-any.whl

Or with:

    .. parsed-literal::

        pip install dxlepoclient-\ |version|\.zip

As an alternative (without PIP), unpack the dxlepoclient-\ |version|\.zip (located in the lib folder) and run the setup
script:

    .. parsed-literal::

        python setup.py install


