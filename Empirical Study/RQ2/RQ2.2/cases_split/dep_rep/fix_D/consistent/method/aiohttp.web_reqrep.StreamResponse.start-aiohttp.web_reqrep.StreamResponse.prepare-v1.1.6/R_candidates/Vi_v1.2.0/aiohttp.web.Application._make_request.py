    def _make_request(self, message, payload, protocol,
                      _cls=web_reqrep.Request):
        return _cls(
            message, payload,
            protocol.transport, protocol.reader, protocol.writer,
            protocol.time_service, protocol._request_handler,
            secure_proxy_ssl_header=self._secure_proxy_ssl_header)
