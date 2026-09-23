    def to_frame(self, filter_observations=True):
        """
        Transform wide format into long (stacked) format as DataFrame

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
            mask = com.notnull(self.values).all(axis=0)
            # size = mask.sum()
            selector = mask.ravel()
        else:
            # size = N * K
            selector = slice(None, None)

        data = {}
        for item in self.items:
            data[item] = self[item].values.ravel()[selector]

        major_labels = np.arange(N).repeat(K)[selector]

        # Anyone think of a better way to do this? np.repeat does not
        # do what I want
        minor_labels = np.arange(K).reshape(1, K)[np.zeros(N, dtype=int)]
        minor_labels = minor_labels.ravel()[selector]

        maj_name = self.major_axis.name or 'major'
        min_name = self.minor_axis.name or 'minor'

        index = MultiIndex(levels=[self.major_axis, self.minor_axis],
                           labels=[major_labels, minor_labels],
                           names=[maj_name, min_name], verify_integrity=False)

        return DataFrame(data, index=index, columns=self.items)
