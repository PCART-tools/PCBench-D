    @staticmethod
    def check(mu, b):
        _value_check(b > 0, "Scale parameter b must be positive.")
        _value_check(mu.is_real, "Location parameter mu should be real")
