    @doc(ExtensionArray.fillna)
    def fillna(
        self,
        value: object | ArrayLike | None = None,
        method: FillnaOptions | None = None,
        limit: int | None = None,
        copy: bool = True,
    ) -> Self:
        value, method = validate_fillna_kwargs(value, method)

        if not self._hasna:
            # TODO(CoW): Not necessary anymore when CoW is the default
            return self.copy()

        if limit is not None:
            return super().fillna(value=value, method=method, limit=limit, copy=copy)

        if method is not None:
            return super().fillna(method=method, limit=limit, copy=copy)

        if isinstance(value, (np.ndarray, ExtensionArray)):
            # Similar to check_value_size, but we do not mask here since we may
            #  end up passing it to the super() method.
            if len(value) != len(self):
                raise ValueError(
                    f"Length of 'value' does not match. Got ({len(value)}) "
                    f" expected {len(self)}"
                )

        try:
            fill_value = self._box_pa(value, pa_type=self._pa_array.type)
        except pa.ArrowTypeError as err:
            msg = f"Invalid value '{str(value)}' for dtype {self.dtype}"
            raise TypeError(msg) from err

        try:
            return type(self)(pc.fill_null(self._pa_array, fill_value=fill_value))
        except pa.ArrowNotImplementedError:
            # ArrowNotImplementedError: Function 'coalesce' has no kernel
            #   matching input types (duration[ns], duration[ns])
            # TODO: remove try/except wrapper if/when pyarrow implements
            #   a kernel for duration types.
            pass

        return super().fillna(value=value, method=method, limit=limit, copy=copy)
