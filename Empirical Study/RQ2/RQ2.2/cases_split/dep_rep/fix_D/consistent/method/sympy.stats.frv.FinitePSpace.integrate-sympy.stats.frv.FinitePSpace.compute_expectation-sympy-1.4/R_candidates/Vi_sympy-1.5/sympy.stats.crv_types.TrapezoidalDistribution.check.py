    @staticmethod
    def check(a, b, c, d):
        _value_check(a < d, "Lower bound parameter a < %s. a = %s"%(d, a))
        _value_check((a <= b, b < c),
        "Level start parameter b must be in range [%s, %s). b = %s"%(a, c, b))
        _value_check((b < c, c <= d),
        "Level end parameter c must be in range (%s, %s]. c = %s"%(b, d, c))
        _value_check(d >= c, "Upper bound parameter d > %s. d = %s"%(c, d))
