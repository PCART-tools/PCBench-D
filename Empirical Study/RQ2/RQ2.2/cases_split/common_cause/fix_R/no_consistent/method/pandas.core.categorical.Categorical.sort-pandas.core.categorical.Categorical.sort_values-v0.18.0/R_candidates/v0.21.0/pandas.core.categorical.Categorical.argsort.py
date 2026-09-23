    def argsort(self, ascending=True, kind='quicksort', *args, **kwargs):
        """
        Returns the indices that would sort the Categorical instance if
        'sort_values' was called. This function is implemented to provide
        compatibility with numpy ndarray objects.

        While an ordering is applied to the category values, arg-sorting
        in this context refers more to organizing and grouping together
        based on matching category values. Thus, this function can be
        called on an unordered Categorical instance unlike the functions
        'Categorical.min' and 'Categorical.max'.

        Returns
        -------
        argsorted : numpy array

        See also
        --------
        numpy.ndarray.argsort
        """
        ascending = nv.validate_argsort_with_ascending(ascending, args, kwargs)
        result = np.argsort(self._codes.copy(), kind=kind, **kwargs)
        if not ascending:
            result = result[::-1]
        return result
