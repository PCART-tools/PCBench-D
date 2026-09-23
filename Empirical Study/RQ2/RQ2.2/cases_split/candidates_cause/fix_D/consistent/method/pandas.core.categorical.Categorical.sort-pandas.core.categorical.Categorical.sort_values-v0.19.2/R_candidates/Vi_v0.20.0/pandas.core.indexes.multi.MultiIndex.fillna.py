    @Appender(ibase._index_shared_docs['fillna'])
    def fillna(self, value=None, downcast=None):
        # isnull is not implemented for MultiIndex
        raise NotImplementedError('isnull is not defined for MultiIndex')
