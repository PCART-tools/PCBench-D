    @staticmethod
    def check(mean, std):
        _value_check(std > 0, "Standard deviation must be positive")
