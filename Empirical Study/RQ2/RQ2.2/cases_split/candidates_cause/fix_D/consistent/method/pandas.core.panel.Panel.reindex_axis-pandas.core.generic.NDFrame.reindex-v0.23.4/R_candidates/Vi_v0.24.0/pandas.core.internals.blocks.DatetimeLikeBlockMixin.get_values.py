    def get_values(self, dtype=None):
        """
        return object dtype as boxed values, such as Timestamps/Timedelta
        """
        if is_object_dtype(dtype):
            values = self.values

            if self.ndim > 1:
                values = values.ravel()

            values = lib.map_infer(values, self._box_func)

            if self.ndim > 1:
                values = values.reshape(self.values.shape)

            return values
        return self.values
