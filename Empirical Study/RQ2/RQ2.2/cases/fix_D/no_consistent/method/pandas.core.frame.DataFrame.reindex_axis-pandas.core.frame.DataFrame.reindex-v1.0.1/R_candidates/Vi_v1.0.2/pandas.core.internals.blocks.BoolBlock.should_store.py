    def should_store(self, value):
        return issubclass(value.dtype.type, np.bool_) and not is_extension_array_dtype(
            value
        )
