Overview
========

The `McAfee ePolicy Orchestrator <https://www.mcafee.com/us/products/epolicy-orchestrator.aspx>`_ (ePO) DXL Python
client library provides a high level wrapper for invoking ePO remote commands via the
`Data Exchange Layer <http://www.mcafee.com/us/solutions/data-exchange-layer.aspx>`_ (DXL) fabric.

The purpose of this library is to allow users to invoke ePO remote commands without having to focus
on lower-level details such as ePO-specific DXL topics and message formats.

This client requires an ePO DXL service to be running and available on the DXL
fabric.

* If version 5.0 or later of the DXL ePO extensions are installed on your ePO
  server, an ePO DXL service should already be running on the fabric.

..

* If you are using an earlier version of the DXL ePO extensions, you can use the
  `McAfee ePolicy Orchestrator (ePO) DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`_.
