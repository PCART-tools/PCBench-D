    def __init__(self, fixed_size):
        _api.check_isinstance(Number, fixed_size=fixed_size)
        self.fixed_size = fixed_size
