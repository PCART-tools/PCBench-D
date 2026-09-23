    def to_frame(self, filter_observations=True):
        """
        Transform wide format into long (stacked) format as DataFrame whose
        columns are the Panel's items and whose index is a MultiIndex formed
        of the Panel's major and minor axes.

        Parameters
        ----------
        filter_observations : boolean, default True
            Drop (major, minor) pairs without a complete set of observations
            across all the items

        Returns
        -------
        y : DataFrame
        """
        _, N, K = self.shape

        if filter_observations:
            # shaped like the return DataFrame
            mask = notna(self.values).all(axis=0)
            # size = mask.sum()
            selector = mask.ravel()
        else:
            # size = N * K
            selector = slice(None, None)

        data = {item: self[item].values.ravel()[selector]
                for item in self.items}

        def construct_multi_parts(idx, n_repeat, n_shuffle=1):
            # Replicates and shuffles MultiIndex, returns individual attributes
            codes = [np.repeat(x, n_repeat) for x in idx.codes]
            # Assumes that each label is divisible by n_shuffle
            codes = [x.reshape(n_shuffle, -1).ravel(order='F')
                     for x in codes]
            codes = [x[selector] for x in codes]
            levels = idx.levels
            names = idx.names
            return codes, levels, names

        def construct_index_parts(idx, major=True):
            levels = [idx]
            if major:
                codes = [np.arange(N).repeat(K)[selector]]
                names = idx.name or 'major'
            else:
                codes = np.arange(K).reshape(1, K)[np.zeros(N, dtype=int)]
                codes = [codes.ravel()[selector]]
                names = idx.name or 'minor'
            names = [names]
            return codes, levels, names

        if isinstance(self.major_axis, MultiIndex):
            major_codes, major_levels, major_names = construct_multi_parts(
                self.major_axis, n_repeat=K)
        else:
            major_codes, major_levels, major_names = construct_index_parts(
                self.major_axis)

        if isinstance(self.minor_axis, MultiIndex):
            minor_codes, minor_levels, minor_names = construct_multi_parts(
                self.minor_axis, n_repeat=N, n_shuffle=K)
        else:
            minor_codes, minor_levels, minor_names = construct_index_parts(
                self.minor_axis, major=False)

        levels = major_levels + minor_levels
        codes = major_codes + minor_codes
        names = major_names + minor_names

        index = MultiIndex(levels=levels, codes=codes, names=names,
                           verify_integrity=False)

        return DataFrame(data, index=index, columns=self.items)
