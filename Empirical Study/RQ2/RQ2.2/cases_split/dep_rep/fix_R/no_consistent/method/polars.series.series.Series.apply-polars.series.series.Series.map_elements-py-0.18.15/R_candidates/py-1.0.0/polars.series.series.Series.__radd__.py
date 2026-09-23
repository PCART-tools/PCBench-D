    def __radd__(self, other: Any) -> Series:
        if isinstance(other, str):
            return (other + self.to_frame()).to_series()
        return self._arithmetic(other, "add", "add_<>_rhs")
