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
            if in_axis and name not in columns:
                result.insert(0, name, lev)

        return result
