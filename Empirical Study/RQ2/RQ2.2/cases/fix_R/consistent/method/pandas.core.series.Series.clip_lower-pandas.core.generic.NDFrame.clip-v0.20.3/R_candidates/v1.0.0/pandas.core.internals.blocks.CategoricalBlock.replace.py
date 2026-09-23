    def replace(
        self,
        to_replace,
        value,
        inplace: bool = False,
        filter=None,
        regex: bool = False,
        convert: bool = True,
    ):
        inplace = validate_bool_kwarg(inplace, "inplace")
        result = self if inplace else self.copy()
        if filter is None:  # replace was called on a series
            result.values.replace(to_replace, value, inplace=True)
            if convert:
                return result.convert(numeric=False, copy=not inplace)
            else:
                return result
        else:  # replace was called on a DataFrame
            if not isna(value):
                result.values.add_categories(value, inplace=True)
            return super(CategoricalBlock, result).replace(
                to_replace, value, inplace, filter, regex, convert
            )
