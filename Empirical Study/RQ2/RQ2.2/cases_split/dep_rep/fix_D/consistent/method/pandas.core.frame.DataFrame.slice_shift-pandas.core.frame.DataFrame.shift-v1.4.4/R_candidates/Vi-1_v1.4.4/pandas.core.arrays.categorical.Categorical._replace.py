    def _replace(self, *, to_replace, value, inplace: bool = False):
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
                    with catch_warnings():
                        simplefilter("ignore")
                        cat.remove_categories(replace_value, inplace=True)
                    continue

                categories = cat.categories.tolist()
                index = categories.index(replace_value)

                if new_value in cat.categories:
                    value_index = categories.index(new_value)
                    cat._codes[cat._codes == index] = value_index
                    with catch_warnings():
                        simplefilter("ignore")
                        cat.remove_categories(replace_value, inplace=True)
                else:
                    categories[index] = new_value
                    with catch_warnings():
                        simplefilter("ignore")
                        cat.rename_categories(categories, inplace=True)
        if not inplace:
            return cat
