    @cache_readonly
    def group_info(self):
        # for compat
        return self.bins, self.binlabels, self.ngroups
