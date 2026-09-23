    @_api.rename_parameter("3.3", "nonpos", "nonpositive")
    def __init__(self, nonpositive='mask'):
        super().__init__()
        self._nonpositive = nonpositive
