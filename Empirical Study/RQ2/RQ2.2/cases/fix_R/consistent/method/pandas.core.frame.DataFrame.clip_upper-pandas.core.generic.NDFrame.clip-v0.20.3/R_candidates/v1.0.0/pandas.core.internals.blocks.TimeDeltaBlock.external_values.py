    def external_values(self, dtype=None):
        return np.asarray(self.values.astype("timedelta64[ns]", copy=False))
