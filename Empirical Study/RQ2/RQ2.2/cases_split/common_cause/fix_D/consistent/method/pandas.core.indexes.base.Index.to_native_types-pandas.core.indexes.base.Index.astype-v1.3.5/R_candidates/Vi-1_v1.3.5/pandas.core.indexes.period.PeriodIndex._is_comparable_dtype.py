    def _is_comparable_dtype(self, dtype: DtypeObj) -> bool:
        """
        Can we compare values of the given dtype to our own?
        """
        if not isinstance(dtype, PeriodDtype):
            return False
        return dtype.freq == self.freq
