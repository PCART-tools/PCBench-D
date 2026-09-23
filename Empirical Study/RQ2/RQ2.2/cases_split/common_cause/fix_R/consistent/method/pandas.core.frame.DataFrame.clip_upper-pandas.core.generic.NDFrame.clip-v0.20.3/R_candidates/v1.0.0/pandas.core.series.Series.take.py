    @Appender(generic.NDFrame.take.__doc__)
    def take(self, indices, axis=0, is_copy=None, **kwargs) -> "Series":
        if is_copy is not None:
            warnings.warn(
                "is_copy is deprecated and will be removed in a future version. "
                "'take' always returns a copy, so there is no need to specify this.",
                FutureWarning,
                stacklevel=2,
            )
        nv.validate_take(tuple(), kwargs)

        indices = ensure_platform_int(indices)
        new_index = self.index.take(indices)

        if is_categorical_dtype(self):
            # https://github.com/pandas-dev/pandas/issues/20664
            # TODO: remove when the default Categorical.take behavior changes
            indices = maybe_convert_indices(indices, len(self._get_axis(axis)))
            kwargs = {"allow_fill": False}
        else:
            kwargs = {}
        new_values = self._values.take(indices, **kwargs)

        return self._constructor(
            new_values, index=new_index, fastpath=True
        ).__finalize__(self)
