    @Appender(_shared_docs['_take'])
    def _take(self, indices, axis=0, convert=True, is_copy=True):
        self._consolidate_inplace()

        if convert:
            indices = maybe_convert_indices(indices, len(self._get_axis(axis)))

        new_data = self._data.take(indices,
                                   axis=self._get_block_manager_axis(axis),
                                   verify=True)
        result = self._constructor(new_data).__finalize__(self)

        # Maybe set copy if we didn't actually change the index.
        if is_copy:
            if not result._get_axis(axis).equals(self._get_axis(axis)):
                result._set_is_copy(self)

        return result
