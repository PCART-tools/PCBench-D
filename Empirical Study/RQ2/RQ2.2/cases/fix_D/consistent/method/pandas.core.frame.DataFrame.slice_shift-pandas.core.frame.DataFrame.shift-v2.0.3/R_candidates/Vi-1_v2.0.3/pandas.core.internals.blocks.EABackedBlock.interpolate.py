    def interpolate(
        self,
        *,
        method: FillnaOptions = "pad",
        axis: int = 0,
        inplace: bool = False,
        limit: int | None = None,
        fill_value=None,
        using_cow: bool = False,
        **kwargs,
    ):
        values = self.values
        if values.ndim == 2 and axis == 0:
            # NDArrayBackedExtensionArray.fillna assumes axis=1
            new_values = values.T.fillna(value=fill_value, method=method, limit=limit).T
        else:
            new_values = values.fillna(value=fill_value, method=method, limit=limit)
        return self.make_block_same_class(new_values)
