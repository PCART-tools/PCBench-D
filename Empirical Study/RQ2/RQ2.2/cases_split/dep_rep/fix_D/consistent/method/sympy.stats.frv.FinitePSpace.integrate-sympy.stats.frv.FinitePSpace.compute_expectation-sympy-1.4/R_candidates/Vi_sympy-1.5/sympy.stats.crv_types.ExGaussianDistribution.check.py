    @staticmethod
    def check(mean, std, rate):
        _value_check(
            std > 0, "Standard deviation of ExGaussian must be positive.")
        _value_check(rate > 0, "Rate of ExGaussian must be positive.")
