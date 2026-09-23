    @classmethod
    def from_array(cls, data, **kwargs):
        """
        Make a Categorical type from a single array-like object.

        For internal compatibility with numpy arrays.

        Parameters
        ----------
        data : array-like
            Can be an Index or array-like. The categories are assumed to be
            the unique values of `data`.
        """
        return Categorical(data, **kwargs)
