    def _validate_searchsorted_value(
        self, value: NumpyValueArrayLike | ExtensionArray
    ) -> NumpyValueArrayLike:
        # TODO(2.0): after deprecation in datetimelikearraymixin is enforced,
        #  we can remove this and use _validate_setitem_value directly
        if isinstance(value, ExtensionArray):
            return value.to_numpy()
        else:
            return value
