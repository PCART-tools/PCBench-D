    @Appender(_index_shared_docs['dropna'])
    def dropna(self, how='any'):
        nans = [level_codes == -1 for level_codes in self.codes]
        if how == 'any':
            indexer = np.any(nans, axis=0)
        elif how == 'all':
            indexer = np.all(nans, axis=0)
        else:
            raise ValueError("invalid how option: {0}".format(how))

        new_codes = [level_codes[~indexer] for level_codes in self.codes]
        return self.copy(codes=new_codes, deep=True)
