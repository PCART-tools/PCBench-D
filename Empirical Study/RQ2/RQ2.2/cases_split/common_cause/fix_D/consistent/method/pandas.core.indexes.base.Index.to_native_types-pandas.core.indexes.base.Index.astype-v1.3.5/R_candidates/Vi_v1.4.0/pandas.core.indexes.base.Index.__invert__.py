    def __invert__(self):
        # GH#8875
        return self._unary_method(operator.inv)
