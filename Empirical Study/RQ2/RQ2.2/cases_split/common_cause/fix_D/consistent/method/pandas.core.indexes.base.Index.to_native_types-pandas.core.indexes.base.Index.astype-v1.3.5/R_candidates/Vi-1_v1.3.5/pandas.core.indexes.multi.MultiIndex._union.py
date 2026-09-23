    def _union(self, other, sort) -> MultiIndex:
        other, result_names = self._convert_can_do_setop(other)
        if (
            any(-1 in code for code in self.codes)
            and any(-1 in code for code in self.codes)
            or self.has_duplicates
            or other.has_duplicates
        ):
            # This is only necessary if both sides have nans or one has dups,
            # fast_unique_multiple is faster
            result = super()._union(other, sort)
        else:
            rvals = other._values.astype(object, copy=False)
            result = lib.fast_unique_multiple([self._values, rvals], sort=sort)

        return MultiIndex.from_arrays(zip(*result), sortorder=0, names=result_names)
