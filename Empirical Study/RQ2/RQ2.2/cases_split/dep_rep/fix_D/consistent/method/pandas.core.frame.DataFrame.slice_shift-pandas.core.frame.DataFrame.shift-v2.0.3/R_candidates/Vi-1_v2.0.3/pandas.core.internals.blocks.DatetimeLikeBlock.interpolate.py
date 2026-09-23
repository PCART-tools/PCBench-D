    def interpolate(
        self,
        *,
        method: FillnaOptions = "pad",
        index: Index | None = None,
        axis: int = 0,
        inplace: bool = False,
        limit: int | None = None,
        fill_value=None,
        using_cow: bool = False,
        **kwargs,
    ):
        values = self.values

        # error: Non-overlapping equality check (left operand type:
        # "Literal['backfill', 'bfill', 'ffill', 'pad']", right operand type:
        # "Literal['linear']")  [comparison-overlap]
        if method == "linear":  # type: ignore[comparison-overlap]
            # TODO: GH#50950 implement for arbitrary EAs
            refs = None
            if using_cow:
                if inplace and not self.refs.has_reference():
                    data_out = values._ndarray
                    refs = self.refs
                else:
                    data_out = values._ndarray.copy()
            else:
                data_out = values._ndarray if inplace else values._ndarray.copy()
            missing.interpolate_array_2d(
                data_out, method=method, limit=limit, index=index, axis=axis
            )
            new_values = type(values)._simple_new(data_out, dtype=values.dtype)
            return self.make_block_same_class(new_values, refs=refs)

        elif values.ndim == 2 and axis == 0:
            # NDArrayBackedExtensionArray.fillna assumes axis=1
            new_values = values.T.fillna(value=fill_value, method=method, limit=limit).T
        else:
            new_values = values.fillna(value=fill_value, method=method, limit=limit)
        return self.make_block_same_class(new_values)
