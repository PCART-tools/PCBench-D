    def _argmin_max(self, skipna: bool, method: str) -> int:
        if self._data.length() in (0, self._data.null_count) or (
            self._hasna and not skipna
        ):
            # For empty or all null, pyarrow returns -1 but pandas expects TypeError
            # For skipna=False and data w/ null, pandas expects NotImplementedError
            # let ExtensionArray.arg{max|min} raise
            return getattr(super(), f"arg{method}")(skipna=skipna)

        if pa_version_under6p0:
            raise NotImplementedError(
                f"arg{method} only implemented for pyarrow version >= 6.0"
            )

        value = getattr(pc, method)(self._data, skip_nulls=skipna)
        return pc.index(self._data, value).as_py()
