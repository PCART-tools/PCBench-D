    def __getitem__(self, key):
        """
        Conserve RangeIndex type for scalar and slice keys.
        """
        if isinstance(key, slice):
            new_range = self._range[key]
            return self._simple_new(new_range, name=self.name)
        elif is_integer(key):
            new_key = int(key)
            try:
                return self._range[new_key]
            except IndexError:
                raise IndexError(
                    "index {key} is out of bounds for axis 0 "
                    "with size {size}".format(key=key, size=len(self))
                )
        elif is_scalar(key):
            raise IndexError(
                "only integers, slices (`:`), "
                "ellipsis (`...`), numpy.newaxis (`None`) "
                "and integer or boolean "
                "arrays are valid indices"
            )
        # fall back to Int64Index
        return super().__getitem__(key)
