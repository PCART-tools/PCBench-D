    def drop(self, labels, errors='raise'):
        """
        Make new Index with passed list of labels deleted

        Parameters
        ----------
        labels : array-like
        errors : {'ignore', 'raise'}, default 'raise'
            If 'ignore', suppress error and existing labels are dropped.

        Returns
        -------
        dropped : Index

        Raises
        ------
        KeyError
            If not all of the labels are found in the selected axis
        """
        arr_dtype = 'object' if self.dtype == 'object' else None
        labels = com._index_labels_to_array(labels, dtype=arr_dtype)
        indexer = self.get_indexer(labels)
        mask = indexer == -1
        if mask.any():
            if errors != 'ignore':
                raise KeyError(
                    '{} not found in axis'.format(labels[mask]))
            indexer = indexer[~mask]
        return self.delete(indexer)
