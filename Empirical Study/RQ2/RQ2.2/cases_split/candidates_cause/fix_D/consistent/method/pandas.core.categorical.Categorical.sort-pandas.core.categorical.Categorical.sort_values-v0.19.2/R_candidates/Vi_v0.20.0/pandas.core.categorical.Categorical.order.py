    def order(self, inplace=False, ascending=True, na_position='last'):
        """
        DEPRECATED: use :meth:`Categorical.sort_values`. That function
        is entirely equivalent to this one.

        See Also
        --------
        Categorical.sort_values
        """
        warn("order is deprecated, use sort_values(...)", FutureWarning,
             stacklevel=2)
        return self.sort_values(inplace=inplace, ascending=ascending,
                                na_position=na_position)
