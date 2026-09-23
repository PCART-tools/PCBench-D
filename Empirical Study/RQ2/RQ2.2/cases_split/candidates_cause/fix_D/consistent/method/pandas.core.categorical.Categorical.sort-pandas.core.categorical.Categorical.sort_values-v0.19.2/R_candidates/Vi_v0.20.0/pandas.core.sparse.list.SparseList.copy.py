    def copy(self):
        """
        Return copy of the list

        Returns
        -------
        new_list : SparseList
        """
        new_splist = SparseList(fill_value=self.fill_value)
        new_splist._chunks = list(self._chunks)
        return new_splist
