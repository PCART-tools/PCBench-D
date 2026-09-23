    def dropna(self):
        """
        Return the Categorical without null values.

        Both missing values (-1 in .codes) and NA as a category are detected.
        NA is removed from the categories if present.

        Returns
        -------
        valid : Categorical
        """
        result = self[self.notna()]
        if isna(result.categories).any():
            result = result.remove_categories([np.nan])
        return result
