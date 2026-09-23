    @cbook._rename_parameter("3.3", "nonpos", "nonpositive")
    def __init__(self, nonpositive='mask'):
        Transform.__init__(self)
        cbook._check_in_list(['mask', 'clip'], nonpositive=nonpositive)
        self._nonpositive = nonpositive
        self._clip = {"clip": True, "mask": False}[nonpositive]
