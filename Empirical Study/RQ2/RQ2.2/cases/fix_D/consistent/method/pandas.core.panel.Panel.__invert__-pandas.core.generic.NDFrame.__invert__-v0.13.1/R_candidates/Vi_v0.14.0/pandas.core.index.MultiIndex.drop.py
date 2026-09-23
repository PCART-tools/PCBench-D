    def drop(self, labels, level=None):
        """
        Make new MultiIndex with passed list of labels deleted

        Parameters
        ----------
        labels : array-like
            Must be a list of tuples
        level : int or level name, default None

        Returns
        -------
        dropped : MultiIndex
        """
        if level is not None:
            return self._drop_from_level(labels, level)

        try:
            if not isinstance(labels, np.ndarray):
                labels = com._index_labels_to_array(labels)
            indexer = self.get_indexer(labels)
            mask = indexer == -1
            if mask.any():
                raise ValueError('labels %s not contained in axis'
                                 % labels[mask])
            return self.delete(indexer)
        except Exception:
            pass

        inds = []
        for label in labels:
            loc = self.get_loc(label)
            if isinstance(loc, int):
                inds.append(loc)
            else:
                inds.extend(lrange(loc.start, loc.stop))

        return self.delete(inds)
