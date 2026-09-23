    @staticmethod
    def check(alpha, beta, sigma):
        _value_check(alpha > 0, "Shape parameter Alpha must be positive.")
        _value_check(beta > 0, "Shape parameter Beta must be positive.")
        _value_check(sigma > 0, "Scale parameter Sigma must be positive.")
