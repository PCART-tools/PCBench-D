    @cache_readonly
    def groups(self) -> dict[Hashable, np.ndarray]:
        """dict {group name -> group labels}"""
        if len(self.groupings) == 1:
            return self.groupings[0].groups
        else:
            to_groupby = []
            for ping in self.groupings:
                gv = ping.grouping_vector
                if not isinstance(gv, BaseGrouper):
                    to_groupby.append(gv)
                else:
                    to_groupby.append(gv.groupings[0].grouping_vector)
            index = MultiIndex.from_arrays(to_groupby)
            return self.axis.groupby(index)
