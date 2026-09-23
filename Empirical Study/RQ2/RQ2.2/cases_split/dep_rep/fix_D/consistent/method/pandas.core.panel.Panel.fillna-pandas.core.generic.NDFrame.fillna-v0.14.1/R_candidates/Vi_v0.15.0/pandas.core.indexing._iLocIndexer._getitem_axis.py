    def _getitem_axis(self, key, axis=0):

        if isinstance(key, slice):
            self._has_valid_type(key, axis)
            return self._get_slice_axis(key, axis=axis)

        elif com._is_bool_indexer(key):
            self._has_valid_type(key, axis)
            return self._getbool_axis(key, axis=axis)

        # a single integer or a list of integers
        else:

            if _is_list_like(key):

                # validate list bounds
                self._is_valid_list_like(key, axis)

                # force an actual list
                key = list(key)

            else:
                key = self._convert_scalar_indexer(key, axis)

                if not com.is_integer(key):
                    raise TypeError("Cannot index by location index with a "
                                    "non-integer key")

                # validate the location
                self._is_valid_integer(key, axis)

            return self._get_loc(key, axis=axis)
