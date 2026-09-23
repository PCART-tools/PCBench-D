    def _get_fingerprint_and_hashfunc(self, req):
        if req.fingerprint:
            return (req.fingerprint, req._hashfunc)
        elif self.fingerprint:
            return (self.fingerprint, self._hashfunc)
        else:
            return (None, None)
