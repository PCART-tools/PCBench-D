    def insert(self, loc, item):
        """
        Make new Index inserting new item at location. Follows
        Python list.append semantics for negative values

        Parameters
        ----------
        loc : int
        item : object

        Returns
        -------
        new_index : Index

        Raises
        ------
        ValueError if the item is not in the categories

        """
        code = self.categories.get_indexer([item])
        if (code == -1) and not (is_scalar(item) and isna(item)):
            raise TypeError(
                "cannot insert an item into a CategoricalIndex "
                "that is not already an existing category"
            )

        codes = self.codes
        codes = np.concatenate((codes[:loc], code, codes[loc:]))
        return self._create_from_codes(codes)
