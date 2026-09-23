    def set_antialiased(self, b):
        """
        True if line should be drawin with antialiased rendering

        ACCEPTS: [True | False]
        """
        if self._antialiased != b:
            self.stale = True
        self._antialiased = b
