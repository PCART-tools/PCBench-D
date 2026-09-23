    def should_store(self, value):
        # when inserting a column should not coerce integers to floats
        # unnecessarily
        return issubclass(value.dtype.type, np.floating) and value.dtype == self.dtype
