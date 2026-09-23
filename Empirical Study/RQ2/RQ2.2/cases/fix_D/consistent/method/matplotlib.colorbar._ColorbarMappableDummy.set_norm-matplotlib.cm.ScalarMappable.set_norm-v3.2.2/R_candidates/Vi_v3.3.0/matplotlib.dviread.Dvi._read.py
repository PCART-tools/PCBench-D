    def _read(self):
        """
        Read one page from the file. Return True if successful,
        False if there were no more pages.
        """
        # Pages appear to start with the sequence
        #   bop (begin of page)
        #   xxx comment
        #   down
        #   push
        #     down, down
        #     push
        #       down (possibly multiple)
        #       push  <=  here, v is the baseline position.
        #         etc.
        # (dviasm is useful to explore this structure.)
        self._baseline_v = None
        while True:
            byte = self.file.read(1)[0]
            self._dtable[byte](self, byte)
            if (self._baseline_v is None
                    and len(getattr(self, "stack", [])) == 3):
                self._baseline_v = self.v
            if byte == 140:                         # end of page
                return True
            if self.state is _dvistate.post_post:   # end of file
                self.close()
                return False
