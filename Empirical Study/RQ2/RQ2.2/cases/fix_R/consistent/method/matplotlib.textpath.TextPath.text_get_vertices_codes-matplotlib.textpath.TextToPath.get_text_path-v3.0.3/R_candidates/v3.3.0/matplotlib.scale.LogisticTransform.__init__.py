    @cbook._rename_parameter("3.3", "nonpos", "nonpositive")
    def __init__(self, nonpositive='mask'):
        Transform.__init__(self)
        self._nonpositive = nonpositive
