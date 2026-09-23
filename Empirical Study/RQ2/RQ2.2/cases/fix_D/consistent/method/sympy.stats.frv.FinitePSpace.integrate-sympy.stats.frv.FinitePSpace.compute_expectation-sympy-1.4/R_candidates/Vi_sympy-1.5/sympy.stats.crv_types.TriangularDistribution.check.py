    @staticmethod
    def check(a, b, c):
        _value_check(b > a, "Parameter b > %s. b = %s"%(a, b))
        _value_check((a <= c, c <= b),
        "Parameter c must be in range [%s, %s]. c = %s"%(a, b, c))
