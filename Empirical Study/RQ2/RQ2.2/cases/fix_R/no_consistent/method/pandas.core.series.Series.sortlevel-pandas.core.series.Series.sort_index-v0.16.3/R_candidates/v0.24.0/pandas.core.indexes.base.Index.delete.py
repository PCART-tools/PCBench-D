    def delete(self, loc):
        """
        Make new Index with passed location(-s) deleted.

        Returns
        -------
        new_index : Index
        """
        return self._shallow_copy(np.delete(self._data, loc))
