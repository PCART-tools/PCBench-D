    def is_saving(self):
        """
        Returns whether the renderer is in the process of saving
        to a file, rather than rendering for an on-screen buffer.
        """
        return self._is_saving
