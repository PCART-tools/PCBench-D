    def unique(self):
        values = self._values

        if not isinstance(values, np.ndarray):
            result: ArrayLike = values.unique()
            if (
                isinstance(self.dtype, np.dtype) and self.dtype.kind in ["m", "M"]
            ) and isinstance(self, ABCSeries):
                # GH#31182 Series._values returns EA
                # unpack numpy datetime for backward-compat
                result = np.asarray(result)
        else:
            result = unique1d(values)

        return result
