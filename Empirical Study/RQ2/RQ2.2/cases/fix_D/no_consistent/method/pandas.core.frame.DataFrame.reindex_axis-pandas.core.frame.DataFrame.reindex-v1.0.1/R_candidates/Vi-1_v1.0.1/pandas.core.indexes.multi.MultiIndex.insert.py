    def insert(self, loc, item):
        """
        Make new MultiIndex inserting new item at location

        Parameters
        ----------
        loc : int
        item : tuple
            Must be same length as number of levels in the MultiIndex

        Returns
        -------
        new_index : Index
        """
        # Pad the key with empty strings if lower levels of the key
        # aren't specified:
        if not isinstance(item, tuple):
            item = (item,) + ("",) * (self.nlevels - 1)
        elif len(item) != self.nlevels:
            raise ValueError("Item must have length equal to number of levels.")

        new_levels = []
        new_codes = []
        for k, level, level_codes in zip(item, self.levels, self.codes):
            if k not in level:
                # have to insert into level
                # must insert at end otherwise you have to recompute all the
                # other codes
                lev_loc = len(level)
                level = level.insert(lev_loc, k)
            else:
                lev_loc = level.get_loc(k)

            new_levels.append(level)
            new_codes.append(np.insert(ensure_int64(level_codes), loc, lev_loc))

        return MultiIndex(
            levels=new_levels, codes=new_codes, names=self.names, verify_integrity=False
        )
