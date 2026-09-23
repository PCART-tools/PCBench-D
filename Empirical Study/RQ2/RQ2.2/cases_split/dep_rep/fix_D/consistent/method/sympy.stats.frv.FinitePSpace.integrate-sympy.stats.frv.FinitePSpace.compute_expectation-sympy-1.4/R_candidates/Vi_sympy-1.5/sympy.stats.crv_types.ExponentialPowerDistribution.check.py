    @staticmethod
    def check(mu, alpha, beta):
        _value_check(alpha > 0, "Scale parameter alpha must be positive.")
        _value_check(beta > 0, "Shape parameter beta must be positive.")
