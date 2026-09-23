    def __rmod__(self, other: Any) -> Series:
        if self.dtype.is_temporal():
            raise TypeError(
                "first cast to integer before applying modulo on datelike dtypes"
            )
        return self._arithmetic(other, "rem", "rem_<>_rhs")
