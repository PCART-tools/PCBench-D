    def _make_request(self, message, payload, protocol, writer, task,
                      _cls=web_request.Request):
        return _cls(
            message, payload, protocol, writer, protocol._time_service, task,
            secure_proxy_ssl_header=self._secure_proxy_ssl_header,
            client_max_size=self._client_max_size)
