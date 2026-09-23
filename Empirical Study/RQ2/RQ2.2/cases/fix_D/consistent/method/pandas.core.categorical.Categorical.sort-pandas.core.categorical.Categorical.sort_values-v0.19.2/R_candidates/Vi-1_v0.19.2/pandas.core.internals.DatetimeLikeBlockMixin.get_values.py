    def get_values(self, dtype=None):
        """
        return object dtype as boxed values, such as Timestamps/Timedelta
        """
        if is_object_dtype(dtype):
            return lib.map_infer(self.values.ravel(),
                                 self._box_func).reshape(self.values.shape)
        return self.values
