    @staticmethod
    def check(d1, d2):
        _value_check((d1 > 0, d1.is_integer),
            "Degrees of freedom d1 must be positive integer.")
        _value_check((d2 > 0, d2.is_integer),
            "Degrees of freedom d2 must be positive integer.")
