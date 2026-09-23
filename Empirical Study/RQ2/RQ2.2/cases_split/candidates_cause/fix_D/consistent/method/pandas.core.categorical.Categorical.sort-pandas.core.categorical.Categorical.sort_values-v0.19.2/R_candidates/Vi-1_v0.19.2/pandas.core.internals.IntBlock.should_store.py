    def should_store(self, value):
        return is_integer_dtype(value) and value.dtype == self.dtype
