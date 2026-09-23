    def __rsub__(self, other: Any) -> Series:
        return self._arithmetic(other, "sub", "sub_<>_rhs")
