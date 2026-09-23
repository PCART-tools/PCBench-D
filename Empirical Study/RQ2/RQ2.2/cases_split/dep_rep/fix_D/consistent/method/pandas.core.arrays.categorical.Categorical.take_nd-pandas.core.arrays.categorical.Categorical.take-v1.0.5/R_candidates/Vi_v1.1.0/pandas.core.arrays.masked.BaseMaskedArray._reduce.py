    def _reduce(self, name: str, skipna: bool = True, **kwargs):
        data = self._data
        mask = self._mask

        if name in {"sum", "prod", "min", "max"}:
            op = getattr(masked_reductions, name)
            return op(data, mask, skipna=skipna, **kwargs)

        # coerce to a nan-aware float if needed
        # (we explicitly use NaN within reductions)
        if self._hasna:
            data = self.to_numpy("float64", na_value=np.nan)

        op = getattr(nanops, "nan" + name)
        result = op(data, axis=0, skipna=skipna, mask=mask, **kwargs)

        if np.isnan(result):
            return libmissing.NA

        return result
