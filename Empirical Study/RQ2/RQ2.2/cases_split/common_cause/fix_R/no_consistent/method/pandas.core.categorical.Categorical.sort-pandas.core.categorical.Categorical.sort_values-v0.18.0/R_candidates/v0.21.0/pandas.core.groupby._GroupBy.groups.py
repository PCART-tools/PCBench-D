    @property
    def groups(self):
        """ dict {group name -> group labels} """
        self._assure_grouper()
        return self.grouper.groups
