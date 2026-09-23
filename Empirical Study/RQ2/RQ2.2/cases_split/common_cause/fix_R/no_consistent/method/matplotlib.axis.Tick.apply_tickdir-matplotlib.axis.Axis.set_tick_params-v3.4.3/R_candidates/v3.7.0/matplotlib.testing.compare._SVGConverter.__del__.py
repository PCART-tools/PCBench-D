    def __del__(self):
        super().__del__()
        if hasattr(self, "_tmpdir"):
            self._tmpdir.cleanup()
