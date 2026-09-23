    @Appender(generic.NDFrame._take.__doc__)
    def _take(self, indices, axis=0, is_copy=False):

        indices = ensure_platform_int(indices)
        new_index = self.index.take(indices)

        if is_categorical_dtype(self):
            # https://github.com/pandas-dev/pandas/issues/20664
            # TODO: remove when the default Categorical.take behavior changes
            indices = maybe_convert_indices(indices, len(self._get_axis(axis)))
            kwargs = {'allow_fill': False}
        else:
            kwargs = {}
        new_values = self._values.take(indices, **kwargs)

        result = (self._constructor(new_values, index=new_index,
                                    fastpath=True).__finalize__(self))

        # Maybe set copy if we didn't actually change the index.
        if is_copy:
            if not result._get_axis(axis).equals(self._get_axis(axis)):
                result._set_is_copy(self)

        return result
