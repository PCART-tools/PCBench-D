    def __init__(self, transport, status,
                 http_version=HttpVersion11, close=False, reason=None):
        super().__init__(transport, http_version, close)

        self._status = status
        if reason is None:
            reason = self.calc_reason(status)

        self._reason = reason
