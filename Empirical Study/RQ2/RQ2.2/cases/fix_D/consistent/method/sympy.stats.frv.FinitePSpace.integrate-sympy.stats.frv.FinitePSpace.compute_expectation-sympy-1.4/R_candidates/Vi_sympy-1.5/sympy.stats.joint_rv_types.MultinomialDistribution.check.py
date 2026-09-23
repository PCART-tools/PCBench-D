    @staticmethod
    def check(n, p):
        _value_check(n > 0,
                        "number of trials must be a positive integer")
        for p_k in p:
            _value_check((p_k >= 0, p_k <= 1),
                        "probability must be in range [0, 1]")
        _value_check(Eq(sum(p), 1),
                        "probabilities must sum to 1")
