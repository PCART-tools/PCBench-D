    def set_status(self, status, reason=None):
        if self.prepared:
            raise RuntimeError("Cannot change the response status code after "
                               "the headers have been sent")
        self._status = int(status)
        if reason is None:
            reason = ResponseImpl.calc_reason(status)
        self._reason = reason
