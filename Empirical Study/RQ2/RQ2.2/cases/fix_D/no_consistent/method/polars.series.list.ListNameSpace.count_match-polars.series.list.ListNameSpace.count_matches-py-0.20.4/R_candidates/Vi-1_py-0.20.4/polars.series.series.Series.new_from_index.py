    def new_from_index(self, index: int, length: int) -> Self:
        """Create a new Series filled with values from the given index."""
        return self._from_pyseries(self._s.new_from_index(index, length))
