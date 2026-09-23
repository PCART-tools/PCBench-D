    def delete(self, loc):
        """
        Make new index with passed location deleted

        Returns
        -------
        new_index : MultiIndex
        """
        new_codes = [np.delete(level_codes, loc) for level_codes in self.codes]
        return MultiIndex(
            levels=self.levels,
            codes=new_codes,
            names=self.names,
            verify_integrity=False,
        )
