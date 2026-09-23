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

        # build a dict of (to replace -> value) pairs
        if is_list_like(to_replace):
            # if to_replace is list-like and value is scalar
            replace_dict = {replace_value: value for replace_value in to_replace}
        else:
            # if both to_replace and value are scalar
            replace_dict = {to_replace: value}

        # other cases, like if both to_replace and value are list-like or if
        # to_replace is a dict, are handled separately in NDFrame
        for replace_value, new_value in replace_dict.items():
            if new_value == replace_value:
                continue
            if replace_value in cat.categories:
                if isna(new_value):
                    cat.remove_categories(replace_value, inplace=True)
                    continue
                categories = cat.categories.tolist()
                index = categories.index(replace_value)
                if new_value in cat.categories:
                    value_index = categories.index(new_value)
                    cat._codes[cat._codes == index] = value_index
                    cat.remove_categories(replace_value, inplace=True)
                else:
                    categories[index] = new_value
                    cat.rename_categories(categories, inplace=True)
        if not inplace:
            return cat
