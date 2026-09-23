    def get_iterator(self, data, axis=0):
        """
        Groupby iterator

        Returns
        -------
        Generator yielding sequence of (name, subsetted object)
        for each group
        """
        if axis == 0:
            start = 0
            for edge, label in zip(self.bins, self.binlabels):
                yield label, data[start:edge]
                start = edge

            if start < len(data):
                yield self.binlabels[-1], data[start:]
        else:
            start = 0
            for edge, label in zip(self.bins, self.binlabels):
                inds = lrange(start, edge)
                yield label, data.take(inds, axis=axis)
                start = edge

            n = len(data.axes[axis])
            if start < n:
                inds = lrange(start, n)
                yield self.binlabels[-1], data.take(inds, axis=axis)
