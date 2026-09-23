    def asof(self, label):
        """
        For a sorted index, return the most recent label up to and including
        the passed label. Return NaN if not found
        """
        if isinstance(label, (Index, ABCSeries, np.ndarray)):
            raise TypeError('%s' % type(label))

        if not isinstance(label, Timestamp):
            label = Timestamp(label)

        if label not in self:
            loc = self.searchsorted(label, side='left')
            if loc > 0:
                return self[loc - 1]
            else:
                return np.nan

        return label
