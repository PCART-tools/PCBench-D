    def order(self, inplace=False, ascending=True, na_position='last', **kwargs):
        """ Sorts the Category by category value returning a new Categorical by default.

        Only ordered Categoricals can be sorted!

        Categorical.sort is the equivalent but sorts the Categorical inplace.

        Parameters
        ----------
        ascending : boolean, default True
            Sort ascending. Passing False sorts descending
        inplace : boolean, default False
            Do operation in place.
        na_position : {'first', 'last'} (optional, default='last')
            'first' puts NaNs at the beginning
            'last' puts NaNs at the end

        Returns
        -------
        y : Category or None

        See Also
        --------
        Category.sort
        """
        if not self.ordered:
            raise TypeError("Categorical not ordered")
        if na_position not in ['last','first']:
            raise ValueError('invalid na_position: {!r}'.format(na_position))

        codes = np.sort(self._codes)
        if not ascending:
            codes = codes[::-1]

        # NaN handling
        na_mask = (codes==-1)
        if na_mask.any():
            n_nans = len(codes[na_mask])
            if na_position=="first" and not ascending:
                # in this case sort to the front
                new_codes = codes.copy()
                new_codes[0:n_nans] = -1
                new_codes[n_nans:] = codes[~na_mask]
                codes = new_codes
            elif na_position=="last" and not ascending:
                # ... and to the end
                new_codes = codes.copy()
                pos = len(codes)-n_nans
                new_codes[0:pos] = codes[~na_mask]
                new_codes[pos:] = -1
                codes = new_codes
        if inplace:
            self._codes = codes
            return
        else:
            return Categorical(values=codes,categories=self.categories, ordered=self.ordered,
                               name=self.name, fastpath=True)
