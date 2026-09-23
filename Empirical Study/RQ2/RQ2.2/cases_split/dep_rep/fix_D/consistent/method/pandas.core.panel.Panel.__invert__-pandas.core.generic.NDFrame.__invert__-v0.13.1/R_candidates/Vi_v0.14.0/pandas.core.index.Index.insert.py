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
        _self = np.asarray(self)
        item_idx = Index([item], dtype=self.dtype).values
        idx = np.concatenate(
            (_self[:loc], item_idx, _self[loc:]))
        return Index(idx, name=self.name)
