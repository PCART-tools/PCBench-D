    def verify(self):
        """Check file integrity"""

        # raise exception if something's wrong.  must be called
        # directly after open, and closes file when finished.
        if self._exclusive_fp:
            self.fp.close()
        self.fp = None
