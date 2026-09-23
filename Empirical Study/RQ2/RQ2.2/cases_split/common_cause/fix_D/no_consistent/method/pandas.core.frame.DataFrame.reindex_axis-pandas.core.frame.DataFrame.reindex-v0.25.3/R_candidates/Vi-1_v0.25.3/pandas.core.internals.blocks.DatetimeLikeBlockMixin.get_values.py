    def get_values(self, dtype=None):
        """
        return object dtype as boxed values, such as Timestamps/Timedelta
        """
        if is_object_dtype(dtype):
            values = self.values.ravel()
            result = self._holder(values).astype(object)
            return result.reshape(self.values.shape)
        return self.values
