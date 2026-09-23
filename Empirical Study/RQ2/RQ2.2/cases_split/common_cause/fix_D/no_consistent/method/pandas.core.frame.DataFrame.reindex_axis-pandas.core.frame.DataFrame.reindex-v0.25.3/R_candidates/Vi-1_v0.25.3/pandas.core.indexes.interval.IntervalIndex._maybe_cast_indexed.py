    def _maybe_cast_indexed(self, key):
        """
        we need to cast the key, which could be a scalar
        or an array-like to the type of our subtype
        """
        if isinstance(key, IntervalIndex):
            return key

        subtype = self.dtype.subtype
        if is_float_dtype(subtype):
            if is_integer(key):
                key = float(key)
            elif isinstance(key, (np.ndarray, Index)):
                key = key.astype("float64")
        elif is_integer_dtype(subtype):
            if is_integer(key):
                key = int(key)

        return key
