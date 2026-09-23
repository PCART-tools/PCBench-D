    def get_chunks(self) -> list[Series]:
        """Get the chunks of this Series as a list of Series."""
        return self._s.get_chunks()
