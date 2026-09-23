    @staticmethod
    def check(mean, shape):
        _value_check(shape > 0, "Shape parameter must be positive")
        _value_check(mean > 0, "Mean must be positive")
