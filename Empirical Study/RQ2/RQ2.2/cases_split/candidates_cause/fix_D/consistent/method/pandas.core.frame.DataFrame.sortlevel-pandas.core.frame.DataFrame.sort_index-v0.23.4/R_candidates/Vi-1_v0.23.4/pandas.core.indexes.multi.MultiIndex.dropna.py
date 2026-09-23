    @Appender(_index_shared_docs['dropna'])
    def dropna(self, how='any'):
        nans = [label == -1 for label in self.labels]
        if how == 'any':
            indexer = np.any(nans, axis=0)
        elif how == 'all':
            indexer = np.all(nans, axis=0)
        else:
            raise ValueError("invalid how option: {0}".format(how))

        new_labels = [label[~indexer] for label in self.labels]
        return self.copy(labels=new_labels, deep=True)
