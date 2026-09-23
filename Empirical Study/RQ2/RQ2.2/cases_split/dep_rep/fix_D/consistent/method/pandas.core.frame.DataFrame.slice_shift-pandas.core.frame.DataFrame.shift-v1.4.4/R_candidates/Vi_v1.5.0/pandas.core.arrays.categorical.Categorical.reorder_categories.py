    def reorder_categories(self, new_categories, ordered=None, inplace=no_default):
        """
        Reorder categories as specified in new_categories.

        `new_categories` need to include all old categories and no new category
        items.

        Parameters
        ----------
        new_categories : Index-like
           The categories in new order.
        ordered : bool, optional
           Whether or not the categorical is treated as a ordered categorical.
           If not given, do not change the ordered information.
        inplace : bool, default False
           Whether or not to reorder the categories inplace or return a copy of
           this categorical with reordered categories.

           .. deprecated:: 1.3.0

        Returns
        -------
        cat : Categorical or None
            Categorical with removed categories or None if ``inplace=True``.

        Raises
        ------
        ValueError
            If the new categories do not contain all old category items or any
            new ones

        See Also
        --------
        rename_categories : Rename categories.
        add_categories : Add new categories.
        remove_categories : Remove the specified categories.
        remove_unused_categories : Remove categories which are not used.
        set_categories : Set the categories to the specified ones.
        """
        if inplace is not no_default:
            warn(
                "The `inplace` parameter in pandas.Categorical."
                "reorder_categories is deprecated and will be removed in "
                "a future version. Reordering categories will always "
                "return a new Categorical object.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
        else:
            inplace = False

        inplace = validate_bool_kwarg(inplace, "inplace")
        if set(self.dtype.categories) != set(new_categories):
            raise ValueError(
                "items in new_categories are not the same as in old categories"
            )

        with catch_warnings():
            simplefilter("ignore")
            return self.set_categories(new_categories, ordered=ordered, inplace=inplace)
