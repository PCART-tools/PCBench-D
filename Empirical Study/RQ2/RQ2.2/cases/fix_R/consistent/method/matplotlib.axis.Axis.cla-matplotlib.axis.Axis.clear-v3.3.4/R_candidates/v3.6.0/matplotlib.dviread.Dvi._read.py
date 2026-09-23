    def _read(self):
        """
        Read one page from the file. Return True if successful,
        False if there were no more pages.
        """
        self._baseline_v = None
        while True:
            byte = self.file.read(1)[0]
            self._dtable[byte](self, byte)
            if byte == 140:                         # end of page
                return True
            if self.state is _dvistate.post_post:   # end of file
                self.close()
                return False
