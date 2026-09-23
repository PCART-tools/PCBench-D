    def sort(self, inplace=True, ascending=True, na_position='last', **kwargs):
        """
        DEPRECATED: use :meth:`Categorical.sort_values`. That function
        is just like this one, except that a new Categorical is returned
        by default, so make sure to pass in 'inplace=True' to get
        inplace sorting.

        See Also
        --------
        Categorical.sort_values
        """
        warn("sort is deprecated, use sort_values(...)", FutureWarning,
             stacklevel=2)
        nv.validate_sort(tuple(), kwargs)
        return self.sort_values(inplace=inplace, ascending=ascending,
                                na_position=na_position)
