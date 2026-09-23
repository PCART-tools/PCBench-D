    @classmethod
    def from_array(cls, data):
        """
        Make a Categorical type from a single array-like object.

        Parameters
        ----------
        data : array-like
            Can be an Index or array-like. The levels are assumed to be
            the unique values of `data`.
        """
        return Categorical(data)
