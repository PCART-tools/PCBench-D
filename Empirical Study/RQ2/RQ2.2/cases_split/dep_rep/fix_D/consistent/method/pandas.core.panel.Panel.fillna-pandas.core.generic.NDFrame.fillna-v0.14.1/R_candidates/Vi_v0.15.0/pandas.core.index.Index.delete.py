    def delete(self, loc):
        """
        Make new Index with passed location(-s) deleted

        Returns
        -------
        new_index : Index
        """
        return Index(np.delete(self._data, loc), name=self.name)
