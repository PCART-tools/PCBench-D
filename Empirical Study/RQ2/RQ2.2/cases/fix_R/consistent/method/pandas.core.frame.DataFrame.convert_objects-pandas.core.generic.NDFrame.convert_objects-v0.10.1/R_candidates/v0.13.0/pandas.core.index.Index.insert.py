    def insert(self, loc, item):
        """
        Make new Index inserting new item at location

        Parameters
        ----------
        loc : int
        item : object

        Returns
        -------
        new_index : Index
        """
        index = np.asarray(self)
        # because numpy is fussy with tuples
        item_idx = Index([item], dtype=index.dtype)
        new_index = np.concatenate((index[:loc], item_idx, index[loc:]))
        return Index(new_index, name=self.name)
