    def values_for_json(self) -> np.ndarray:
        # special casing datetimetz to avoid conversion through
        #  object dtype
        return self.values._ndarray
