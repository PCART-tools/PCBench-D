    def get_values(self, dtype=None):
        # return object dtypes as Timedelta
        if dtype == object:
            return lib.map_infer(self.values.ravel(), lib.Timedelta
                                 ).reshape(self.values.shape)
        return self.values
