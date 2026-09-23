    def __exit__(self, *args):
        if hasattr(self, "fp") and getattr(self, "_exclusive_fp", False):
            if getattr(self, "_fp", False):
                if self._fp != self.fp:
                    self._fp.close()
                self._fp = DeferredError(ValueError("Operation on closed image"))
            if self.fp:
                self.fp.close()
        self.fp = None
