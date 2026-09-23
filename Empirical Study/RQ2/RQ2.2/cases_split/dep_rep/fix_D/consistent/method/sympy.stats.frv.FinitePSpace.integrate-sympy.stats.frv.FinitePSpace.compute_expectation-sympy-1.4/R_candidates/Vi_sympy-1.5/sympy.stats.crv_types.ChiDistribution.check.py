    @staticmethod
    def check(k):
        _value_check(k > 0, "Number of degrees of freedom (k) must be positive.")
        _value_check(k.is_integer, "Number of degrees of freedom (k) must be an integer.")
