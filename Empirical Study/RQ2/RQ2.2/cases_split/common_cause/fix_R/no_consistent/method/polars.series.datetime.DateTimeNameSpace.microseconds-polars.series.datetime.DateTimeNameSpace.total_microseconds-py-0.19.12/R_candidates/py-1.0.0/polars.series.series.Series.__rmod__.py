    def __rmod__(self, other: Any) -> Series:
        if self.dtype.is_temporal():
            msg = "first cast to integer before applying modulo on datelike dtypes"
            raise TypeError(msg)
        return self._arithmetic(other, "rem", "rem_<>_rhs")
