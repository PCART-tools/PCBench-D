    @staticmethod
    def check(p, a, b):
        _value_check(p > 0, "Shape parameter p must be positive.")
        _value_check(a > 0, "Shape parameter a must be positive.")
        _value_check(b > 0, "Scale parameter b must be positive.")
