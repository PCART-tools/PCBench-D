    @Appender(ibase._index_shared_docs['fillna'])
    def fillna(self, value=None, downcast=None):
        # isna is not implemented for MultiIndex
        raise NotImplementedError('isna is not defined for MultiIndex')
