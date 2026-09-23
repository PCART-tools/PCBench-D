    def delete(self, loc):
        """
        Make new Index with passed location(-s) deleted

        Returns
        -------
        new_index : Index
        """
        return self._create_from_codes(np.delete(self.codes, loc))
