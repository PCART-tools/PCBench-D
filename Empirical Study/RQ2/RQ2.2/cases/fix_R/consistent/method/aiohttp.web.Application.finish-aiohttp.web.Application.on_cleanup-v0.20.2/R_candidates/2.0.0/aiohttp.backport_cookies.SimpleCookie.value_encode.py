    def value_encode(self, val):  # pragma: no cover
        strval = str(val)
        return strval, _quote(strval)
