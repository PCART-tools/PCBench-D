    @cache_readonly
    def label_info(self):
        # return the labels of items in original grouped axis
        labels, _, _ = self.group_info
        if self.indexer is not None:
            sorter = np.lexsort((labels, self.indexer))
            labels = labels[sorter]
        return labels
