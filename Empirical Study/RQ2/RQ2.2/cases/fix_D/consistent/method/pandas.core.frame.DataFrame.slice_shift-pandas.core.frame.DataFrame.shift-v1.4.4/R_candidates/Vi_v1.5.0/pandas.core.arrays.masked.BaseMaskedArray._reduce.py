    def _reduce(self, name: str, *, skipna: bool = True, **kwargs):
        if name in {"any", "all", "min", "max", "sum", "prod"}:
            return getattr(self, name)(skipna=skipna, **kwargs)

        data = self._data
        mask = self._mask

        if name in {"mean"}:
            op = getattr(masked_reductions, name)
            result = op(data, mask, skipna=skipna, **kwargs)
            return result

        # coerce to a nan-aware float if needed
        # (we explicitly use NaN within reductions)
        if self._hasna:
            data = self.to_numpy("float64", na_value=np.nan)

        # median, var, std, skew, kurt, idxmin, idxmax
        op = getattr(nanops, "nan" + name)
        result = op(data, axis=0, skipna=skipna, mask=mask, **kwargs)

        if np.isnan(result):
            return libmissing.NA

        return result
