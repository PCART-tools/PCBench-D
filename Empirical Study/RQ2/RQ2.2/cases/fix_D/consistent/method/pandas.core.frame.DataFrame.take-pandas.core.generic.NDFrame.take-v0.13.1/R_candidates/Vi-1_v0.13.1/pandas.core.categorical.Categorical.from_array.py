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
        if isinstance(data, Index) and hasattr(data, 'factorize'):
            labels, levels = data.factorize()
        else:
            try:
                labels, levels = factorize(data, sort=True)
            except TypeError:
                labels, levels = factorize(data, sort=False)

        return Categorical(labels, levels,
                           name=getattr(data, 'name', None))
