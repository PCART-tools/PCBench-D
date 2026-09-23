    def to_dense(self):
        # Categorical.get_values returns a DatetimeIndex for datetime
        # categories, so we can't simply use `np.asarray(self.values)` like
        # other types.
        return self.values._internal_get_values()
