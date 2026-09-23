    @staticmethod
    def check(p):
        _value_check(And(0 < p, p <= 1), "p must be between 0 and 1")
