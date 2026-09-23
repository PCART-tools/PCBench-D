    def close(self):
        """
        Close the underlying file if it is open.
        """
        if not self.file.closed:
            self.file.close()
