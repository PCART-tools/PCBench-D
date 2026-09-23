    def _start(self, request):
        if not self._chunked and hdrs.CONTENT_LENGTH not in self._headers:
            if not self._body_payload:
                if self._body is not None:
                    self._headers[hdrs.CONTENT_LENGTH] = str(len(self._body))
                else:
                    self._headers[hdrs.CONTENT_LENGTH] = '0'

        return super()._start(request)
