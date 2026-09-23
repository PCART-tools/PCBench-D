    @cbook._rename_parameter("3.3", "nonpos", "nonpositive")
    def __init__(self, base, nonpositive='clip'):
        Transform.__init__(self)
        if base <= 0 or base == 1:
            raise ValueError('The log base cannot be <= 0 or == 1')
        self.base = base
        self._clip = cbook._check_getitem(
            {"clip": True, "mask": False}, nonpositive=nonpositive)
