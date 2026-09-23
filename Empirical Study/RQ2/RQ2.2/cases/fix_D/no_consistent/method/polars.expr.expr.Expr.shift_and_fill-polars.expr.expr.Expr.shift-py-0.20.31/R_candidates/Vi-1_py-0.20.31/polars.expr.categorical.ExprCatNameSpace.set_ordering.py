    @deprecate_function(
        "Set the ordering directly on the datatype `pl.Categorical('lexical')`"
        " or `pl.Categorical('physical')` or `cast()` to the intended data type."
        " This method will be removed in the next breaking change",
        version="0.19.19",
    )
    def set_ordering(self, ordering: CategoricalOrdering) -> Expr:
        """
        Determine how this categorical series should be sorted.

        Parameters
        ----------
        ordering : {'physical', 'lexical'}
            Ordering type:

            - 'physical' -> Use the physical representation of the categories to
              determine the order (default).
            - 'lexical' -> Use the string values to determine the ordering.
        """
        return wrap_expr(self._pyexpr.cat_set_ordering(ordering))
