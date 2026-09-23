    def _transform(
        self, result, values, comp_ids, transform_func, is_datetimelike: bool, **kwargs
    ):

        comp_ids, _, ngroups = self.group_info
        transform_func(result, values, comp_ids, ngroups, is_datetimelike, **kwargs)

        return result
