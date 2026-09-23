    def _convert_to_indexer(self, obj, axis=0, is_setter=False):
        """ much simpler as we only have to deal with our valid types """

        # make need to convert a float key
        if isinstance(obj, slice):
            return self._convert_slice_indexer(obj, axis)

        elif is_float(obj):
            return self._convert_scalar_indexer(obj, axis)

        elif self._has_valid_type(obj, axis):
            return obj

        raise ValueError("Can only index by location with a [%s]" %
                         self._valid_types)
