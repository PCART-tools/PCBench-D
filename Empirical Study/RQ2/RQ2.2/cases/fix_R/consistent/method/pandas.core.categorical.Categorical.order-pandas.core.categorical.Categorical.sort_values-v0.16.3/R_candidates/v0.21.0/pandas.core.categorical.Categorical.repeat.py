    def repeat(self, repeats, *args, **kwargs):
        """
        Repeat elements of a Categorical.

        See also
        --------
        numpy.ndarray.repeat

        """
        nv.validate_repeat(args, kwargs)
        codes = self._codes.repeat(repeats)
        return self._constructor(values=codes, categories=self.categories,
                                 ordered=self.ordered, fastpath=True)
