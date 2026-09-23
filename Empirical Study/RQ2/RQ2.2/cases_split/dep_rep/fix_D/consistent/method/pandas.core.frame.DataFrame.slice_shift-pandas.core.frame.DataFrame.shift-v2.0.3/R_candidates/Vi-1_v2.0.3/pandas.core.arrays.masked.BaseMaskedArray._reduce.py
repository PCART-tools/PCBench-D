    def _reduce(self, name: str, *, skipna: bool = True, **kwargs):
        if name in {"any", "all", "min", "max", "sum", "prod", "mean", "var", "std"}:
            return getattr(self, name)(skipna=skipna, **kwargs)

        data = self._data
        mask = self._mask

        # median, skew, kurt, sem
        op = getattr(nanops, f"nan{name}")
        result = op(data, axis=0, skipna=skipna, mask=mask, **kwargs)

        if np.isnan(result):
            return libmissing.NA

        return result
