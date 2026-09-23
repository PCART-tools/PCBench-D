    @cache_readonly
    def groups(self):
        """ dict {group name -> group labels} """
        if len(self.groupings) == 1:
            return self.groupings[0].groups
        else:
            to_groupby = lzip(*(ping.grouper for ping in self.groupings))
            to_groupby = Index(to_groupby)
            return self.axis.groupby(to_groupby)
