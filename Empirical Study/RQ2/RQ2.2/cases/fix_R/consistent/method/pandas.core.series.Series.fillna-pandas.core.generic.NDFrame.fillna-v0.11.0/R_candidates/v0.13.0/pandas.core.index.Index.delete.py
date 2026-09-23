    def delete(self, loc):
        """
        Make new Index with passed location deleted

        Returns
        -------
        new_index : Index
        """
        arr = np.delete(self.values, loc)
        return Index(arr)
