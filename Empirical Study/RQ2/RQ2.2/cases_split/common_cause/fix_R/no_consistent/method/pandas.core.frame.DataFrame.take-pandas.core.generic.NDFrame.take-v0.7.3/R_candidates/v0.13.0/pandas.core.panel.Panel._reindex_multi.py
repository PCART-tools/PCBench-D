    def _reindex_multi(self, axes, copy, fill_value):
        """ we are guaranteed non-Nones in the axes! """
        items = axes['items']
        major = axes['major_axis']
        minor = axes['minor_axis']
        a0, a1, a2 = len(items), len(major), len(minor)

        values = self.values
        new_values = np.empty((a0, a1, a2), dtype=values.dtype)

        new_items, indexer0 = self.items.reindex(items)
        new_major, indexer1 = self.major_axis.reindex(major)
        new_minor, indexer2 = self.minor_axis.reindex(minor)

        if indexer0 is None:
            indexer0 = lrange(len(new_items))

        if indexer1 is None:
            indexer1 = lrange(len(new_major))

        if indexer2 is None:
            indexer2 = lrange(len(new_minor))

        for i, ind in enumerate(indexer0):
            com.take_2d_multi(values[ind], (indexer1, indexer2),
                              out=new_values[i])

        return Panel(new_values, items=new_items, major_axis=new_major,
                     minor_axis=new_minor)
