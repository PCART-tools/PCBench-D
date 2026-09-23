    def should_store(self, value):
        return not (issubclass(value.dtype.type,
                               (np.integer, np.floating, np.complexfloating,
                                np.datetime64, np.bool_)) or
                    # TODO(ExtensionArray): remove is_extension_type
                    # when all extension arrays have been ported.
                    is_extension_type(value) or
                    is_extension_array_dtype(value))
