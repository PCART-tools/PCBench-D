    def get_values(self, dtype=None):
        """
        return an internal format, currently just the ndarray
        this is often overridden to handle to_dense like operations
        """
        if is_object_dtype(dtype):
            return self.values.astype(object)
        return self.values
