    def reorder_levels(self, order) -> MultiIndex:
        """
        Rearrange levels using input order. May not drop or duplicate levels.

        Parameters
        ----------
        order : list of int or list of str
            List representing new level order. Reference level by number
            (position) or by key (label).

        Returns
        -------
        MultiIndex

        Examples
        --------
        >>> mi = pd.MultiIndex.from_arrays([[1, 2], [3, 4]], names=['x', 'y'])
        >>> mi
        MultiIndex([(1, 3),
                    (2, 4)],
                   names=['x', 'y'])

        >>> mi.reorder_levels(order=[1, 0])
        MultiIndex([(3, 1),
                    (4, 2)],
                   names=['y', 'x'])

        >>> mi.reorder_levels(order=['y', 'x'])
        MultiIndex([(3, 1),
                    (4, 2)],
                   names=['y', 'x'])
        """
        order = [self._get_level_number(i) for i in order]
        if len(order) != self.nlevels:
            raise AssertionError(
                f"Length of order must be same as number of levels ({self.nlevels}), "
                f"got {len(order)}"
            )
        new_levels = [self.levels[i] for i in order]
        new_codes = [self.codes[i] for i in order]
        new_names = [self.names[i] for i in order]

        return MultiIndex(
            levels=new_levels, codes=new_codes, names=new_names, verify_integrity=False
        )
