    @classmethod
    def _add_accessors(cls):
        """ add in Categorical accessor methods """

        from pandas.core.arrays import Categorical
        CategoricalIndex._add_delegate_accessors(
            delegate=Categorical, accessors=["rename_categories",
                                             "reorder_categories",
                                             "add_categories",
                                             "remove_categories",
                                             "remove_unused_categories",
                                             "set_categories",
                                             "as_ordered", "as_unordered",
                                             "min", "max"],
            typ='method', overwrite=True)
