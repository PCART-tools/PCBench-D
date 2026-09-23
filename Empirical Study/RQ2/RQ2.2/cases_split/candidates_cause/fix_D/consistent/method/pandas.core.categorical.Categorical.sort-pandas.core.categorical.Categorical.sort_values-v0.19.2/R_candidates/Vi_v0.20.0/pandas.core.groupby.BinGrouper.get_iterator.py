    def get_iterator(self, data, axis=0):
        """
        Groupby iterator

        Returns
        -------
        Generator yielding sequence of (name, subsetted object)
        for each group
        """
        if isinstance(data, NDFrame):
            slicer = lambda start, edge: data._slice(
                slice(start, edge), axis=axis)
            length = len(data.axes[axis])
        else:
            slicer = lambda start, edge: data[slice(start, edge)]
            length = len(data)

        start = 0
        for edge, label in zip(self.bins, self.binlabels):
            if label is not NaT:
                yield label, slicer(start, edge)
            start = edge

        if start < length:
            yield self.binlabels[-1], slicer(start, None)
