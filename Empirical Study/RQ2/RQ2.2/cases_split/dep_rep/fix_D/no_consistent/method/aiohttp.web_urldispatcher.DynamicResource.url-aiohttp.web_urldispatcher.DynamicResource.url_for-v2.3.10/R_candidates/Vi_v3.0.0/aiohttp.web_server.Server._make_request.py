    def _make_request(self, message, payload, protocol, writer, task):
        return BaseRequest(
            message, payload, protocol, writer, task, self._loop)
