    @staticmethod
    def check(a, s, m):
        _value_check(a > 0, "Shape parameter alpha must be positive.")
        _value_check(s > 0, "Scale parameter s must be positive.")
