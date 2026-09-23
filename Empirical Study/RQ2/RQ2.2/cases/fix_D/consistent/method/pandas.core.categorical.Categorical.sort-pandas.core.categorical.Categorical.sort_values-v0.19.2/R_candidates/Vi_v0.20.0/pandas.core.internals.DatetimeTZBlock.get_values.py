    def get_values(self, dtype=None):
        # return object dtype as Timestamps with the zones
        if is_object_dtype(dtype):
            f = lambda x: lib.Timestamp(x, tz=self.values.tz)
            return lib.map_infer(
                self.values.ravel(), f).reshape(self.values.shape)
        return self.values
