    def to_hierarchical(self, n_repeat, n_shuffle=1):
        """
        Return a MultiIndex reshaped to conform to the
        shapes given by n_repeat and n_shuffle.

        .. deprecated:: 0.24.0

        Useful to replicate and rearrange a MultiIndex for combination
        with another Index with n_repeat items.

        Parameters
        ----------
        n_repeat : int
            Number of times to repeat the labels on self
        n_shuffle : int
            Controls the reordering of the labels. If the result is going
            to be an inner level in a MultiIndex, n_shuffle will need to be
            greater than one. The size of each label must divisible by
            n_shuffle.

        Returns
        -------
        MultiIndex

        Examples
        --------
        >>> idx = pd.MultiIndex.from_tuples([(1, 'one'), (1, 'two'),
                                            (2, 'one'), (2, 'two')])
        >>> idx.to_hierarchical(3)
        MultiIndex([(1, 'one'),
                    (1, 'one'),
                    (1, 'one'),
                    (1, 'two'),
                    (1, 'two'),
                    (1, 'two'),
                    (2, 'one'),
                    (2, 'one'),
                    (2, 'one'),
                    (2, 'two'),
                    (2, 'two'),
                    (2, 'two')],
                   )
        """
        levels = self.levels
        codes = [np.repeat(level_codes, n_repeat) for level_codes in self.codes]
        # Assumes that each level_codes is divisible by n_shuffle
        codes = [x.reshape(n_shuffle, -1).ravel(order="F") for x in codes]
        names = self.names
        warnings.warn(
            "Method .to_hierarchical is deprecated and will "
            "be removed in a future version",
            FutureWarning,
            stacklevel=2,
        )
        return MultiIndex(levels=levels, codes=codes, names=names)
