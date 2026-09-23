    @staticmethod
    def check(n, theta):
        _value_check((n > 0),
                        "sample size should be positive integer.")
        _value_check(theta.is_positive, "mutation rate should be positive.")
