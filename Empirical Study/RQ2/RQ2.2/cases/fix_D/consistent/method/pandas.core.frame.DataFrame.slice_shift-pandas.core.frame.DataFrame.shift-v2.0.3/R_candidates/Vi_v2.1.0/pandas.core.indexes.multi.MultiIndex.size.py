    @property
    def size(self) -> int:
        """
        Return the number of elements in the underlying data.
        """
        # override Index.size to avoid materializing _values
        return len(self)
