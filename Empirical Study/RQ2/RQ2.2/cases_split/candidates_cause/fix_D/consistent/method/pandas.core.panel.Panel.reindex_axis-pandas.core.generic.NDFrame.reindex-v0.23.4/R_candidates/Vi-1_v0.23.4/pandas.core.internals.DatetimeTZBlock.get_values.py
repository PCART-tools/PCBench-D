    def get_values(self, dtype=None):
        # return object dtype as Timestamps with the zones
        if is_object_dtype(dtype):
            return lib.map_infer(
                self.values.ravel(), self._box_func).reshape(self.values.shape)
        return self.values
