    @cache_readonly
    def groups(self) -> dict[Hashable, np.ndarray]:
        """dict {group name -> group labels}"""
        if len(self.groupings) == 1:
            return self.groupings[0].groups
        else:
            to_groupby = zip(*(ping.grouping_vector for ping in self.groupings))
            index = Index(to_groupby)
            return self.axis.groupby(index)
