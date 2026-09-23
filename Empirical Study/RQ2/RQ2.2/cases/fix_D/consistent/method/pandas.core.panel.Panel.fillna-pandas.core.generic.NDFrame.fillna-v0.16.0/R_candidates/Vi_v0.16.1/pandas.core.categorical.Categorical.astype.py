    def astype(self, dtype):
        """ coerce this type to another dtype """
        if is_categorical_dtype(dtype):
            return self
        return np.array(self, dtype=dtype)
