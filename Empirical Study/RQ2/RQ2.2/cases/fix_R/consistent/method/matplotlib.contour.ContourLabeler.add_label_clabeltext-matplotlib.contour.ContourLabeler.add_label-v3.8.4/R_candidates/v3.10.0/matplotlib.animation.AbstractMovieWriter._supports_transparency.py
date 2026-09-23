    def _supports_transparency(self):
        """
        Whether this writer supports transparency.

        Writers may consult output file type and codec to determine this at runtime.
        """
        return False
