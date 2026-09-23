    @property
    def groups(self):
        """
        Dict {group name -> group labels}.
        """
        self._assure_grouper()
        return self.grouper.groups
