    def replace(self, to_replace, value, inplace=False, filter=None,
                regex=False):
        to_replace_values = np.atleast_1d(to_replace)
        if not np.can_cast(to_replace_values, bool):
            to_replace = to_replace_values
        return super(BoolBlock, self).replace(to_replace, value,
                                              inplace=inplace, filter=filter,
                                              regex=regex)
