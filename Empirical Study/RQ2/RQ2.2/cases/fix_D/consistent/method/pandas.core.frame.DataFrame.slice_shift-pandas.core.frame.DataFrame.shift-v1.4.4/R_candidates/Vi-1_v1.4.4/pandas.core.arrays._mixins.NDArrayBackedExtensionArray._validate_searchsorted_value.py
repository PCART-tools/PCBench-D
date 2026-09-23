    def _validate_searchsorted_value(
        self, value: NumpyValueArrayLike | ExtensionArray
    ) -> NumpyValueArrayLike:
        if isinstance(value, ExtensionArray):
            return value.to_numpy()
        else:
            return value
