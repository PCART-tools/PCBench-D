    def _close_fp(self):
        if getattr(self, "_fp", False) and not isinstance(self._fp, DeferredError):
            if self._fp != self.fp:
                self._fp.close()
            self._fp = DeferredError(ValueError("Operation on closed image"))
        if self.fp:
            self.fp.close()
