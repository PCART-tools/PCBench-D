    @property
    def ngroups(self):
        self._assure_grouper()
        return self.grouper.ngroups
