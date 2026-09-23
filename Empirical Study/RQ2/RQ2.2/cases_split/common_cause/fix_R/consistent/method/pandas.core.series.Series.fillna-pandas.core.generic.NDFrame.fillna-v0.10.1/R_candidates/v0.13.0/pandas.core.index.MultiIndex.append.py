    def append(self, other):
        """
        Append a collection of Index options together

        Parameters
        ----------
        other : Index or list/tuple of indices

        Returns
        -------
        appended : Index
        """
        if not isinstance(other, (list, tuple)):
            other = [other]

        to_concat = (self.values,) + tuple(k.values for k in other)
        new_tuples = np.concatenate(to_concat)

        # if all(isinstance(x, MultiIndex) for x in other):
        try:
            return MultiIndex.from_tuples(new_tuples, names=self.names)
        except:
            return Index(new_tuples)
