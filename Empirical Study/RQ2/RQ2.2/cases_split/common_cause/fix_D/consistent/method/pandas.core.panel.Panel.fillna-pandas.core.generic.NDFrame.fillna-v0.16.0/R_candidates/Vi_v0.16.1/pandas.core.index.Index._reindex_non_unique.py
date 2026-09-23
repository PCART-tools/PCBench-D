    def _reindex_non_unique(self, target):
        """
        *this is an internal non-public method*

        Create a new index with target's values (move/add/delete values as necessary)
        use with non-unique Index and a possibly non-unique target

        Parameters
        ----------
        target : an iterable

        Returns
        -------
        new_index : pd.Index
            Resulting index
        indexer : np.ndarray or None
            Indices of output values in original index

        """

        target = _ensure_index(target)
        indexer, missing = self.get_indexer_non_unique(target)
        check = indexer != -1
        new_labels = self.take(indexer[check])
        new_indexer = None

        if len(missing):
            l = np.arange(len(indexer))

            missing = com._ensure_platform_int(missing)
            missing_labels = target.take(missing)
            missing_indexer = com._ensure_int64(l[~check])
            cur_labels = self.take(indexer[check]).values
            cur_indexer = com._ensure_int64(l[check])

            new_labels = np.empty(tuple([len(indexer)]), dtype=object)
            new_labels[cur_indexer] = cur_labels
            new_labels[missing_indexer] = missing_labels

            # a unique indexer
            if target.is_unique:

                # see GH5553, make sure we use the right indexer
                new_indexer = np.arange(len(indexer))
                new_indexer[cur_indexer] = np.arange(len(cur_labels))
                new_indexer[missing_indexer] = -1

            # we have a non_unique selector, need to use the original
            # indexer here
            else:

                # need to retake to have the same size as the indexer
                indexer = indexer.values
                indexer[~check] = 0

                # reset the new indexer to account for the new size
                new_indexer = np.arange(len(self.take(indexer)))
                new_indexer[~check] = -1

        return self._shallow_copy(new_labels), indexer, new_indexer
