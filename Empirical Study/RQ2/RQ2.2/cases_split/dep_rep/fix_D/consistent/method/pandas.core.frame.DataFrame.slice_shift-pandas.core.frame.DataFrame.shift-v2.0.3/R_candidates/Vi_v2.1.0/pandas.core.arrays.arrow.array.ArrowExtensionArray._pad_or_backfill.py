    def _pad_or_backfill(
        self, *, method: FillnaOptions, limit: int | None = None, copy: bool = True
    ) -> Self:
        if not self._hasna:
            # TODO(CoW): Not necessary anymore when CoW is the default
            return self.copy()

        if limit is None:
            method = missing.clean_fill_method(method)
            try:
                if method == "pad":
                    return type(self)(pc.fill_null_forward(self._pa_array))
                elif method == "backfill":
                    return type(self)(pc.fill_null_backward(self._pa_array))
            except pa.ArrowNotImplementedError:
                # ArrowNotImplementedError: Function 'coalesce' has no kernel
                #   matching input types (duration[ns], duration[ns])
                # TODO: remove try/except wrapper if/when pyarrow implements
                #   a kernel for duration types.
                pass

        # TODO(3.0): after EA.fillna 'method' deprecation is enforced, we can remove
        #  this method entirely.
        return super()._pad_or_backfill(method=method, limit=limit, copy=copy)
