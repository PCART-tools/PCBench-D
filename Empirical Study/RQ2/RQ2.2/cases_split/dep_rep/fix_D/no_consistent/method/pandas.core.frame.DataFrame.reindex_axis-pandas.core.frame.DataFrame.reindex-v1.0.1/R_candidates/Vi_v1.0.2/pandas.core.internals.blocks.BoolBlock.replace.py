    def replace(
        self, to_replace, value, inplace=False, filter=None, regex=False, convert=True
    ):
        inplace = validate_bool_kwarg(inplace, "inplace")
        to_replace_values = np.atleast_1d(to_replace)
        if not np.can_cast(to_replace_values, bool):
            return self
        return super().replace(
            to_replace,
            value,
            inplace=inplace,
            filter=filter,
            regex=regex,
            convert=convert,
        )
