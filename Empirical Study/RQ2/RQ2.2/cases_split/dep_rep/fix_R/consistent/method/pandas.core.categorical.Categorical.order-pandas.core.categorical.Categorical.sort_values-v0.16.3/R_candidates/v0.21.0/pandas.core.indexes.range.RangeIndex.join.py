    @Appender(_index_shared_docs['join'])
    def join(self, other, how='left', level=None, return_indexers=False,
             sort=False):
        if how == 'outer' and self is not other:
            # note: could return RangeIndex in more circumstances
            return self._int64index.join(other, how, level, return_indexers,
                                         sort)

        return super(RangeIndex, self).join(other, how, level, return_indexers,
                                            sort)
