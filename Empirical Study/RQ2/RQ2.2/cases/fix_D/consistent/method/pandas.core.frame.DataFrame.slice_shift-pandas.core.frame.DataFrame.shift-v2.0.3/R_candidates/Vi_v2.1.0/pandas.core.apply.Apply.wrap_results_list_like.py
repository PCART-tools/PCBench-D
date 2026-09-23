    def wrap_results_list_like(
        self, keys: list[Hashable], results: list[Series | DataFrame]
    ):
        from pandas.core.reshape.concat import concat

        obj = self.obj

        try:
            return concat(results, keys=keys, axis=1, sort=False)
        except TypeError as err:
            # we are concatting non-NDFrame objects,
            # e.g. a list of scalars
            from pandas import Series

            result = Series(results, index=keys, name=obj.name)
            if is_nested_object(result):
                raise ValueError(
                    "cannot combine transform and aggregation operations"
                ) from err
            return result
