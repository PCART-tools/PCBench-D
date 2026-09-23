    @staticmethod
    def check(a, b):
        _value_check(b > a, "Parameter b must be in range (%s, oo)."%(a))
