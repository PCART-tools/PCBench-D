    @staticmethod
    def check(mean, std):
        _value_check(std > 0, "Parameter std must be positive.")
