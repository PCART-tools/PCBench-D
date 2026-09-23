    def get_values(self, dtype=None):
        # return object dtype as Timestamps
        if dtype == object:
            return lib.map_infer(self.values.ravel(), lib.Timestamp)\
                      .reshape(self.values.shape)
        return self.values
