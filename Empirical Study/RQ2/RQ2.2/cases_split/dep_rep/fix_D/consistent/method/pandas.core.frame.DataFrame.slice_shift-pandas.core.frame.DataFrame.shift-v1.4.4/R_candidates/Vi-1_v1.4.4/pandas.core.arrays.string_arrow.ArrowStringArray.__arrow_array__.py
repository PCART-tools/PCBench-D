    def __arrow_array__(self, type=None):
        """Convert myself to a pyarrow Array or ChunkedArray."""
        return self._data
