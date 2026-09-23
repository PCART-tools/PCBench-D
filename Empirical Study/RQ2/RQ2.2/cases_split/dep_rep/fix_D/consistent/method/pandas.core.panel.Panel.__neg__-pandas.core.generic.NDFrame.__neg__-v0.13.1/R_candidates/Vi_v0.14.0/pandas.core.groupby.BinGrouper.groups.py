    @cache_readonly
    def groups(self):
        """ dict {group name -> group labels} """

        # this is mainly for compat
        # GH 3881
        return dict(zip(self.binlabels,self.bins))
