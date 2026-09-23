    def unique(self):
        values = self._values

        if not isinstance(values, np.ndarray):
            result: ArrayLike = values.unique()
            if self.dtype.kind in ["m", "M"] and isinstance(self, ABCSeries):
                # GH#31182 Series._values returns EA, unpack for backward-compat
                if getattr(self.dtype, "tz", None) is None:
                    result = np.asarray(result)
        else:
            result = unique1d(values)

        return result
