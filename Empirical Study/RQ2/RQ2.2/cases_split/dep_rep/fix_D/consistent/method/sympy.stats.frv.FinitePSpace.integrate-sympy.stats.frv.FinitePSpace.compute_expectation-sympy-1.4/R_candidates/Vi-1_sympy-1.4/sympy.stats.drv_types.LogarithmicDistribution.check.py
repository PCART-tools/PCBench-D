    @staticmethod
    def check(p):
        _value_check(And(p > 0, p < 1), "p should be between 0 and 1")
