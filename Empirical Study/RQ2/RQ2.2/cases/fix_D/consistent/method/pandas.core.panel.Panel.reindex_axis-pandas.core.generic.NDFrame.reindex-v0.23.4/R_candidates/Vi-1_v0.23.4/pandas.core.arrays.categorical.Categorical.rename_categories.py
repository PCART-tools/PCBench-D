    def rename_categories(self, new_categories, inplace=False):
        """ Renames categories.

        Raises
        ------
        ValueError
            If new categories are list-like and do not have the same number of
            items than the current categories or do not validate as categories

        Parameters
        ----------
        new_categories : list-like, dict-like or callable

           * list-like: all items must be unique and the number of items in
             the new categories must match the existing number of categories.

           * dict-like: specifies a mapping from
             old categories to new. Categories not contained in the mapping
             are passed through and extra categories in the mapping are
             ignored.

             .. versionadded:: 0.21.0

           * callable : a callable that is called on all items in the old
             categories and whose return values comprise the new categories.

             .. versionadded:: 0.23.0

           .. warning::

              Currently, Series are considered list like. In a future version
              of pandas they'll be considered dict-like.

        inplace : boolean (default: False)
           Whether or not to rename the categories inplace or return a copy of
           this categorical with renamed categories.

        Returns
        -------
        cat : Categorical or None
           With ``inplace=False``, the new categorical is returned.
           With ``inplace=True``, there is no return value.

        See also
        --------
        reorder_categories
        add_categories
        remove_categories
        remove_unused_categories
        set_categories

        Examples
        --------
        >>> c = Categorical(['a', 'a', 'b'])
        >>> c.rename_categories([0, 1])
        [0, 0, 1]
        Categories (2, int64): [0, 1]

        For dict-like ``new_categories``, extra keys are ignored and
        categories not in the dictionary are passed through

        >>> c.rename_categories({'a': 'A', 'c': 'C'})
        [A, A, b]
        Categories (2, object): [A, b]

        You may also provide a callable to create the new categories

        >>> c.rename_categories(lambda x: x.upper())
        [A, A, B]
        Categories (2, object): [A, B]
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        cat = self if inplace else self.copy()

        if isinstance(new_categories, ABCSeries):
            msg = ("Treating Series 'new_categories' as a list-like and using "
                   "the values. In a future version, 'rename_categories' will "
                   "treat Series like a dictionary.\n"
                   "For dict-like, use 'new_categories.to_dict()'\n"
                   "For list-like, use 'new_categories.values'.")
            warn(msg, FutureWarning, stacklevel=2)
            new_categories = list(new_categories)

        if is_dict_like(new_categories):
            cat.categories = [new_categories.get(item, item)
                              for item in cat.categories]
        elif callable(new_categories):
            cat.categories = [new_categories(item) for item in cat.categories]
        else:
            cat.categories = new_categories
        if not inplace:
            return cat
