    def _insert_inaxis_grouper_inplace(self, result):
        # zip in reverse so we can always insert at loc 0
        izip = zip(* map(reversed, (
            self.grouper.names,
            self.grouper.get_group_levels(),
            [grp.in_axis for grp in self.grouper.groupings])))

        for name, lev, in_axis in izip:
            if in_axis:
                result.insert(0, name, lev)
