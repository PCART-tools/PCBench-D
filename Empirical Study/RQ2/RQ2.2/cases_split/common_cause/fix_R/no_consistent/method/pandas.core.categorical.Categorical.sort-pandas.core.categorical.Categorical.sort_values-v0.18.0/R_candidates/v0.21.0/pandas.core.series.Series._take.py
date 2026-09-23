    @Appender(generic._shared_docs['_take'])
    def _take(self, indices, axis=0, convert=True, is_copy=False):
        if convert:
            indices = maybe_convert_indices(indices, len(self._get_axis(axis)))

        indices = _ensure_platform_int(indices)
        new_index = self.index.take(indices)
        new_values = self._values.take(indices)

        result = (self._constructor(new_values, index=new_index,
                                    fastpath=True).__finalize__(self))

        # Maybe set copy if we didn't actually change the index.
        if is_copy:
            if not result._get_axis(axis).equals(self._get_axis(axis)):
                result._set_is_copy(self)

        return result
