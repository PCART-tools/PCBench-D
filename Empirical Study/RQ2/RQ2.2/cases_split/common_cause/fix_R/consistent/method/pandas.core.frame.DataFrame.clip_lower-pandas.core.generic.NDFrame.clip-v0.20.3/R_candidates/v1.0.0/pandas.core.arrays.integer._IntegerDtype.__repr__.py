    def __repr__(self) -> str:
        sign = "U" if self.is_unsigned_integer else ""
        return f"{sign}Int{8 * self.itemsize}Dtype()"
