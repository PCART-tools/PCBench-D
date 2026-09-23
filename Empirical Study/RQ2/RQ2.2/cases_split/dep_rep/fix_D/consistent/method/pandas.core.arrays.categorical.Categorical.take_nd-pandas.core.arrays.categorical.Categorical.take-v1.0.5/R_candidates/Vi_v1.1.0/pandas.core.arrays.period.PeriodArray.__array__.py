    def __array__(self, dtype=None) -> np.ndarray:
        if dtype == "i8":
            return self.asi8
        elif dtype == bool:
            return ~self._isnan

        # This will raise TypeError for non-object dtypes
        return np.array(list(self), dtype=object)
