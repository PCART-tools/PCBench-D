    def order(self, inplace=False, ascending=True, na_position='last'):
        """
        DEPRECATED: use :meth:`Categorical.sort_values`

        Sorts the Category by category value returning a new Categorical by default.

        Only ordered Categoricals can be sorted!

        Categorical.sort is the equivalent but sorts the Categorical inplace.

        Parameters
        ----------
        inplace : boolean, default False
            Do operation in place.
        ascending : boolean, default True
            Sort ascending. Passing False sorts descending
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
        warn("order is deprecated, use sort_values(...)",
             FutureWarning, stacklevel=2)
        return self.sort_values(inplace=inplace, ascending=ascending, na_position=na_position)
