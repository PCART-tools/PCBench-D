    def __repr__(self):
        sign = "U" if self.is_unsigned_integer else ""
        return "{sign}Int{size}Dtype()".format(sign=sign, size=8 * self.itemsize)
