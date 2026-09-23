    def interpolate(
        self, method="pad", axis=0, inplace=False, limit=None, fill_value=None, **kwargs
    ):
        values = self.values
        if values.ndim == 2 and axis == 0:
            # NDArrayBackedExtensionArray.fillna assumes axis=1
            new_values = values.T.fillna(value=fill_value, method=method, limit=limit).T
        else:
            new_values = values.fillna(value=fill_value, method=method, limit=limit)
        return self.make_block_same_class(new_values)
