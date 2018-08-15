from dxlclient.service import ServiceRegistrationInfo
from tests.mock_requesthandlers import *


class MockEpoServer(object):
    def __init__(self, client, id_number=0, use_commands_service=True):
        self._client = client
        self.id_number = id_number
        self.use_commands_service = use_commands_service

        # Create DXL Service Registration object
        self._service_registration_info = ServiceRegistrationInfo(
            self._client,
            "/mcafee/service/epo/commands"
            if self.use_commands_service else "/mcafee/service/epo/remote"
        )
        self._service_registration_info._ttl_lower_limit = 5
        self._service_registration_info.ttl = 5
        if self.use_commands_service:
            self._service_registration_info.metadata = \
                {"epoGuid": LOCAL_TEST_SERVER_NAME + str(id_number)}

    def __enter__(self):
        mock_callback = FakeEpoServerCallback(self._client,
                                              self.id_number,
                                              self.use_commands_service)

        self._service_registration_info.add_topic(
            mock_callback.epo_request_topic,
            mock_callback
        )

        self._client.register_service_sync(self._service_registration_info, 10)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.unregister_service_sync(self._service_registration_info,
                                             10)
