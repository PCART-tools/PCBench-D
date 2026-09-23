    @staticmethod
    def validate_categories(categories, fastpath=False):
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
        from pandas import Index

        if not fastpath and not is_list_like(categories):
            msg = "Parameter 'categories' must be list-like, was {!r}"
            raise TypeError(msg.format(categories))
        elif not isinstance(categories, ABCIndexClass):
            categories = Index(categories, tupleize_cols=False)

        if not fastpath:

            if categories.hasnans:
                raise ValueError('Categorial categories cannot be null')

            if not categories.is_unique:
                raise ValueError('Categorical categories must be unique')

        if isinstance(categories, ABCCategoricalIndex):
            categories = categories.categories

        return categories
