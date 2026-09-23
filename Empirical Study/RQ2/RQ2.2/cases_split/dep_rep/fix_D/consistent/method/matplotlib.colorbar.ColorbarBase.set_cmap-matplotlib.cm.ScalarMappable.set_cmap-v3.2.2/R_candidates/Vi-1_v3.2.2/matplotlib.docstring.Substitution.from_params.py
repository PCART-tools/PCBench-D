    @classmethod
    def from_params(cls, params):
        """
        In the case where the params is a mutable sequence (list or
        dictionary) and it may change before this class is called, one may
        explicitly use a reference to the params rather than using *args or
        **kwargs which will copy the values and not reference them.
        """
        result = cls()
        result.params = params
        return result
