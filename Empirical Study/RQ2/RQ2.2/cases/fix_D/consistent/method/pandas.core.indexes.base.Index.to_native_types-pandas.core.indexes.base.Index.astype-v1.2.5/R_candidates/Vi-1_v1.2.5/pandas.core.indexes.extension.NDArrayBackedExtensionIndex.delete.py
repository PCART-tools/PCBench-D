    def delete(self, loc):
        """
        Make new Index with passed location(-s) deleted

        Returns
        -------
        new_index : Index
        """
        new_vals = np.delete(self._data._ndarray, loc)
        arr = self._data._from_backing_data(new_vals)
        return type(self)._simple_new(arr, name=self.name)
