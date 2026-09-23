    def set_status(self, status, reason=None, _RESPONSES=RESPONSES):
        assert not self.prepared, \
            'Cannot change the response status code after ' \
            'the headers have been sent'
        self._status = int(status)
        if reason is None:
            try:
                reason = _RESPONSES[self._status][0]
            except:
                reason = ''
        self._reason = reason
