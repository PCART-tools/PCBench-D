    def sort(self, inplace=True, ascending=True, na_position='last'):
        """ Sorts the Category inplace by category value.

        Only ordered Categoricals can be sorted!

        Catgorical.order is the equivalent but returns a new Categorical.

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
        Category.sort_values
        """
        return self.sort_values(inplace=inplace, ascending=ascending,
                                na_position=na_position)
