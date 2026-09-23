    @property
    def indices(self):
        """ dict {group name -> group indices} """
        self._assure_grouper()
        return self.grouper.indices
