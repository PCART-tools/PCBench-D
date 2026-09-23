    @staticmethod
    def check(mu, omega):
        _value_check(mu >= S.Half, "Shape parameter mu must be greater than equal to 1/2.")
        _value_check(omega > 0, "Spread parameter omega must be positive.")
