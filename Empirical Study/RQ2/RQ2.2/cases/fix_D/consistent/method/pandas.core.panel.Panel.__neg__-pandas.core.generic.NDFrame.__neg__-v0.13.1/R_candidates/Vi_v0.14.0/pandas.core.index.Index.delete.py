    def delete(self, loc):
        """
        Make new Index with passed location(-s) deleted

        Returns
        -------
        new_index : Index
        """
        return np.delete(self, loc)
