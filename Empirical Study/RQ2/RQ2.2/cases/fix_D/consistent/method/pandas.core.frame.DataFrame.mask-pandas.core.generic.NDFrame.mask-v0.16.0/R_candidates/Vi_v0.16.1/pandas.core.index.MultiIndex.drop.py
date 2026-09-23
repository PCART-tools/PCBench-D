    def drop(self, labels, level=None, errors='raise'):
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
            if not isinstance(labels, (np.ndarray, Index)):
                labels = com._index_labels_to_array(labels)
            indexer = self.get_indexer(labels)
            mask = indexer == -1
            if mask.any():
                if errors != 'ignore':
                    raise ValueError('labels %s not contained in axis'
                                     % labels[mask])
                indexer = indexer[~mask]
        except Exception:
            pass

        inds = []
        for label in labels:
            try:
                loc = self.get_loc(label)
                if isinstance(loc, int):
                    inds.append(loc)
                else:
                    inds.extend(lrange(loc.start, loc.stop))
            except KeyError:
                if errors != 'ignore':
                    raise

        return self.delete(inds)
