    @staticmethod
    def validate_categories(categories, fastpath: bool = False):
        """
        Validates that we have good categories

        Parameters
        ----------
        categories : array-like
        fastpath : bool
            Whether to skip nan and uniqueness checks

        Returns
        -------
        categories : Index
        """
        from pandas.core.indexes.base import Index

        if not fastpath and not is_list_like(categories):
            raise TypeError(
                f"Parameter 'categories' must be list-like, was {repr(categories)}"
            )
        elif not isinstance(categories, ABCIndexClass):
            categories = Index(categories, tupleize_cols=False)

        if not fastpath:

            if categories.hasnans:
                raise ValueError("Categorial categories cannot be null")

            if not categories.is_unique:
                raise ValueError("Categorical categories must be unique")

        if isinstance(categories, ABCCategoricalIndex):
            categories = categories.categories

        return categories
