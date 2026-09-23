    @staticmethod
    def check(p, succ, fail):
        _value_check((p >= 0, p <= 1),
                    "p should be in range [0, 1].")
