    def replace(self, to_replace, value, inplace: bool = False):
        """
        Replaces all instances of one value with another

        Parameters
        ----------
        to_replace: object
            The value to be replaced

        value: object
            The value to replace it with

        inplace: bool
            Whether the operation is done in-place

        Returns
        -------
        None if inplace is True, otherwise the new Categorical after replacement


        Examples
        --------
        >>> s = pd.Categorical([1, 2, 1, 3])
        >>> s.replace(1, 3)
        [3, 3, 2, 3]
        Categories (2, int64): [2, 3]
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        cat = self if inplace else self.copy()
        if to_replace in cat.categories:
            if isna(value):
                cat.remove_categories(to_replace, inplace=True)
            else:
                categories = cat.categories.tolist()
                index = categories.index(to_replace)
                if value in cat.categories:
                    value_index = categories.index(value)
                    cat._codes[cat._codes == index] = value_index
                    cat.remove_categories(to_replace, inplace=True)
                else:
                    categories[index] = value
                    cat.rename_categories(categories, inplace=True)
        if not inplace:
            return cat
