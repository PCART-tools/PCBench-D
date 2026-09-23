    def _make_request(self, message, payload, protocol):
        return BaseRequest(
            message, payload,
            protocol.transport, protocol.reader, protocol.writer,
            protocol.time_service, protocol._request_handler)
