    def __exit__(self, *args):
        if hasattr(self, "fp"):
            if getattr(self, "_exclusive_fp", False):
                self._close_fp()
            self.fp = None
