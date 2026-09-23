    @staticmethod
    def check(alpha, beta, lamda):
        _value_check(alpha > 0, "Shape parameter Alpha must be positive.")
        _value_check(beta > 0, "Shape parameter Beta must be positive.")
        _value_check(lamda >= 0, "Noncentrality parameter Lambda must be positive")
