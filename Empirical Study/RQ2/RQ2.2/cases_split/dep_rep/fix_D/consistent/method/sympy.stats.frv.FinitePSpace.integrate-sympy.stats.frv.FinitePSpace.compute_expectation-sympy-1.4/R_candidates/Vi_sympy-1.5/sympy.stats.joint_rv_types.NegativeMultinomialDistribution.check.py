    @staticmethod
    def check(k0, p):
        _value_check(k0 > 0,
                        "number of failures must be a positive integer")
        for p_k in p:
            _value_check((p_k >= 0, p_k <= 1),
                        "probability must be in range [0, 1].")
        _value_check(sum(p) <= 1,
                        "success probabilities must not be greater than 1.")
