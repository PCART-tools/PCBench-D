    @_api.rename_parameter("3.3", "nonpos", "nonpositive")
    def __init__(self, base, nonpositive='clip'):
        super().__init__()
        if base <= 0 or base == 1:
            raise ValueError('The log base cannot be <= 0 or == 1')
        self.base = base
        self._clip = _api.check_getitem(
            {"clip": True, "mask": False}, nonpositive=nonpositive)
