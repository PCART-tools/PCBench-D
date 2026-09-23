    @property
    def indices(self):
        """
        Dict {group name -> group indices}.
        """
        self._assure_grouper()
        return self.grouper.indices
