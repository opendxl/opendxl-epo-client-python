Authorization
=============

A critical aspect of exposing ePO remote commands to the DXL fabric is adding
an authorization policy that restricts which clients can invoke the service.
This section walks through the steps to create an ``authorization`` for a
Python-based DXL client to invoke an ePO remote command.

.. note::

    The steps below apply when version 5.0 or later of the DXL ePO extensions
    have been installed on an ePO server. If you are using an older version of
    the DXL ePO extensions, you will need to use a standalone
    `ePO DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`_
    to proxy remote commands to an ePO server. For command authorization
    using the ``ePO DXL Python Service`` see the following document:

    `<https://opendxl.github.io/opendxl-epo-service-python/pydoc/authorization.html#client-authorization>`_

Python-based DXL clients are identified by their certificates. Client-specific
certificates and/or Certificate Authorities (CAs) can be used to limit which
clients can invoke ePO remote commands. A client certificate can be used to
establish a restriction for a single client whereas a certificate authority can
be used to establish a restriction for all clients that were signed by that
particular authority.

If you are using the
`External Certificate Authority (CA) Provisioning <https://opendxl.github.io/opendxl-client-python/pydoc/epoexternalcertissuance.html>`_
approach to manage your DXL client certificates, you will need to manually
import your client certificate into ePO in order to be able to create an ePO
remote command ``authorization`` for the certificate. For more information on
importing client certificates into ePO, see the
`ePO Certificate Authority (CA) Import <https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html>`_
section in the OpenDXL Python Client SDK documentation.

The following section walks through the steps to create an ``authorization``
for an ePO remote command.

#. Navigate to **Server Settings** and select the **DXL Commands** setting
   on the left navigation bar.

   .. image:: commandauth1.png

#. Click the **Edit** button in the lower right corner (as shown in the image
   above).

   .. image:: commandauth2.png

#. In the command tree in the left column, select an individual or group of
   remote command(s) for which the authorization should be created.

   If a certificate is granted authorization at a group level, the certificate
   can be used to run each of the commands with the group's subtree. In the
   example below, the top-level ``ePO`` group is selected. This enables the
   certificate to be used for running all remote commands.

    .. note::

        It is recommended to create authorizations for the minimal set of
        remote commands which need to be accessible to the DXL fabric.

#. Click the **Actions** button in the lower left corner (as shown in the image
   above).

   .. image:: commandauth3.png

#. In the **Actions** drop-down list, select the **Create Authorization**
   option.

   .. image:: commandauth4.png

#. Select the **User** that the command(s) should be run as on the ePO server
   and select the checkboxes in the **Restrict to ...** sections for the
   desired entities which should be authorized to run the command(s).

   To authorize the DXL Python client to run the remote command, select the
   check box for the corresponding Certificate Authority or client certificate.

    .. note::

        It is recommended to create authorizations for the least privileged
        user account and the minimal set of client certificates needed to
        perform the selected remote command(s).

   .. image:: commandauth5.png

#. Click the **OK** button in the lower right corner (as shown in the image
   above).

   .. image:: commandauth6.png

#. Click the **Save** button in the lower right corner (as shown in the image
   above).

   .. image:: commandauth7.png

The remote command(s) should now be able to be performed with the authorized
certificates.
