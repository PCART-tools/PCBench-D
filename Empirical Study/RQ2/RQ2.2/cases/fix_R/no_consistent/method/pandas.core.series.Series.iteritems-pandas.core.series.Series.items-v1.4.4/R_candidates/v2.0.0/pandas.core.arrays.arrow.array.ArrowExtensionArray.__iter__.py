    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over elements of the array.
        """
        na_value = self._dtype.na_value
        for value in self._data:
            val = value.as_py()
            if val is None:
                yield na_value
            else:
                yield val
