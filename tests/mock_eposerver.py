from dxlclient.service import ServiceRegistrationInfo
from tests.mock_requesthandlers import *

class MockEpoServer(object):
    def __init__(self, client, id_number=0):
        self._client = client
        self.id_number = id_number

        # Create DXL Service Registration object
        self._service_registration_info = ServiceRegistrationInfo(
            self._client,
            "/mcafee/service/epo/remote",
        )
        self._service_registration_info._ttl_lower_limit = 5
        self._service_registration_info.ttl = 5

    def start_service(self):
        mock_callback = FakeEpoServerCallback(self._client, self.id_number)

        self._service_registration_info.add_topic(
            mock_callback.EPO_REQUEST_TOPIC,
            mock_callback
        )

        self._client.register_service_sync(self._service_registration_info, 10)

    def stop_service(self):
        self._client.unregister_service_sync(self._service_registration_info, 10)
