    @classmethod
    def _validate_categories(cls, categories):
        """" Validates that we have good categories """
        if not isinstance(categories, Index):
            dtype = None
            if not hasattr(categories, "dtype"):
                categories = _convert_to_list_like(categories)
                # on categories with NaNs, int values would be converted to float.
                # Use "object" dtype to prevent this.
                if isnull(categories).any():
                    without_na = np.array([x for x in categories if notnull(x)])
                    with_na = np.array(categories)
                    if with_na.dtype != without_na.dtype:
                        dtype = "object"
            categories = Index(categories, dtype=dtype)
        if not categories.is_unique:
            raise ValueError('Categorical categories must be unique')
        return categories
