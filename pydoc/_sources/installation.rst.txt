Library Installation
====================

Prerequisites
*************

* OpenDXL Python Client library installed
    `<https://github.com/opendxl/opendxl-client-python>`_

* The OpenDXL Python Client prerequisites must be satisfied
    `<https://opendxl.github.io/opendxl-client-python/pydoc/installation.html>`_

* McAfee ePolicy Orchestrator (ePO) service is running and available on DXL fabric
    `<https://github.com/opendxl/opendxl-epo-service-python>`_ (Python-based service implementation)

* OpenDXL Python Client has permission to invoke ePO remote commands
    `<https://opendxl.github.io/opendxl-epo-service-python/pydoc/authorization.html#client-authorization>`_

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


