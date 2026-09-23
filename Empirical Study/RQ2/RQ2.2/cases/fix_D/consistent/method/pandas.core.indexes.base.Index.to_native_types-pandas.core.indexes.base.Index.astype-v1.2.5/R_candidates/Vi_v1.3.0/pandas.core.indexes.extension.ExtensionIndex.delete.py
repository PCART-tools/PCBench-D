    def delete(self, loc):
        """
        Make new Index with passed location(-s) deleted

        Returns
        -------
        new_index : Index
        """
        arr = self._data.delete(loc)
        return type(self)._simple_new(arr, name=self.name)
