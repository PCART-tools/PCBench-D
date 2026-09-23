    @cache_readonly
    def _reso(self) -> int:
        """
        The NPY_DATETIMEUNIT corresponding to this dtype's resolution.
        """
        reso = {
            "s": dtypes.NpyDatetimeUnit.NPY_FR_s,
            "ms": dtypes.NpyDatetimeUnit.NPY_FR_ms,
            "us": dtypes.NpyDatetimeUnit.NPY_FR_us,
            "ns": dtypes.NpyDatetimeUnit.NPY_FR_ns,
        }[self._unit]
        return reso.value
