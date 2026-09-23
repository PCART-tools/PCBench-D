    @cache_readonly
    def groups(self):
        """ dict {group name -> group labels} """

        # this is mainly for compat
        # GH 3881
        result = {key: value for key, value in zip(self.binlabels, self.bins)
                  if key is not NaT}
        return result
