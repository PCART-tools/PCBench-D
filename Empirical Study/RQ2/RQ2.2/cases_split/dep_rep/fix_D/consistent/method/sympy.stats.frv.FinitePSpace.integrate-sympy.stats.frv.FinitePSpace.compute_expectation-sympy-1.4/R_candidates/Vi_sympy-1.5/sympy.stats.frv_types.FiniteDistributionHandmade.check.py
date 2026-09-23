    @staticmethod
    def check(density):
        for p in density.values():
            _value_check((p >= 0, p <= 1),
                        "Probability at a point must be between 0 and 1.")
        _value_check(Eq(sum(density.values()), 1), "Total Probability must be 1.")
