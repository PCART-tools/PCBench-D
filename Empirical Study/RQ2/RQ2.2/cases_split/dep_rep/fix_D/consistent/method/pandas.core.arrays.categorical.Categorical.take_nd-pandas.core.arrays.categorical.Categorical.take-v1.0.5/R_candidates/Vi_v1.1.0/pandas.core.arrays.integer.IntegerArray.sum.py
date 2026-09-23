    def sum(self, skipna=True, min_count=0, **kwargs):
        nv.validate_sum((), kwargs)
        result = masked_reductions.sum(
            values=self._data, mask=self._mask, skipna=skipna, min_count=min_count
        )
        return result
