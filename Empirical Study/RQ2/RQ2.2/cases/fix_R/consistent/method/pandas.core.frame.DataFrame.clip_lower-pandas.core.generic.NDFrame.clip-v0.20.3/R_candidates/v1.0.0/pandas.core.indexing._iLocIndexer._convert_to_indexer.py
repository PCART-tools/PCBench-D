    def _convert_to_indexer(self, obj, axis: int, raise_missing: bool = False):
        """
        Much simpler as we only have to deal with our valid types.
        """
        # make need to convert a float key
        if isinstance(obj, slice):
            return self._convert_slice_indexer(obj, axis)

        elif is_float(obj):
            return self._convert_scalar_indexer(obj, axis)

        try:
            self._validate_key(obj, axis)
            return obj
        except ValueError:
            raise ValueError(f"Can only index by location with a [{self._valid_types}]")
