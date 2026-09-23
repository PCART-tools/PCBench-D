    @classmethod
    def _validate_categories(cls, categories, fastpath=False):
        """
        Validates that we have good categories

        Parameters
        ----------
        fastpath : boolean (default: False)
           Don't perform validation of the categories for uniqueness or nulls

        """
        if not isinstance(categories, ABCIndexClass):
            dtype = None
            if not hasattr(categories, "dtype"):
                categories = _convert_to_list_like(categories)
                # On categories with NaNs, int values would be converted to
                # float. Use "object" dtype to prevent this.
                if isnull(categories).any():
                    without_na = np.array([x for x in categories
                                           if notnull(x)])
                    with_na = np.array(categories)
                    if with_na.dtype != without_na.dtype:
                        dtype = "object"

            from pandas import Index
            categories = Index(categories, dtype=dtype)

        if not fastpath:

            # check properties of the categories
            # we don't allow NaNs in the categories themselves

            if categories.hasnans:
                # NaNs in cats deprecated in 0.17,
                # remove in 0.18 or 0.19 GH 10748
                msg = ('\nSetting NaNs in `categories` is deprecated and '
                       'will be removed in a future version of pandas.')
                warn(msg, FutureWarning, stacklevel=3)

            # categories must be unique

            if not categories.is_unique:
                raise ValueError('Categorical categories must be unique')

        return categories
