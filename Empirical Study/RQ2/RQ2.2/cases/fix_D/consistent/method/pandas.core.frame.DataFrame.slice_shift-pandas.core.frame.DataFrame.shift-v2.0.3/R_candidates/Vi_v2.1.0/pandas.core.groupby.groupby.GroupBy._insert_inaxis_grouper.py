    @final
    def _insert_inaxis_grouper(self, result: Series | DataFrame) -> DataFrame:
        if isinstance(result, Series):
            result = result.to_frame()

        # zip in reverse so we can always insert at loc 0
        columns = result.columns
        for name, lev, in_axis in zip(
            reversed(self.grouper.names),
            reversed(self.grouper.get_group_levels()),
            reversed([grp.in_axis for grp in self.grouper.groupings]),
        ):
            # GH #28549
            # When using .apply(-), name will be in columns already
            if name not in columns:
                if in_axis:
                    result.insert(0, name, lev)
                else:
                    msg = (
                        "A grouping was used that is not in the columns of the "
                        "DataFrame and so was excluded from the result. This grouping "
                        "will be included in a future version of pandas. Add the "
                        "grouping as a column of the DataFrame to silence this warning."
                    )
                    warnings.warn(
                        message=msg,
                        category=FutureWarning,
                        stacklevel=find_stack_level(),
                    )

        return result
