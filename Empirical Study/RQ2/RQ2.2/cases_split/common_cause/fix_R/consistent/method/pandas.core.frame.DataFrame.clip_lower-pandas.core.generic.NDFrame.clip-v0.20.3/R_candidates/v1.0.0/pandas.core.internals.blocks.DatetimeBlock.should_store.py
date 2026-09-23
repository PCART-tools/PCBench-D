    def should_store(self, value):
        return (
            issubclass(value.dtype.type, np.datetime64)
            and not is_datetime64tz_dtype(value)
            and not is_extension_array_dtype(value)
        )
