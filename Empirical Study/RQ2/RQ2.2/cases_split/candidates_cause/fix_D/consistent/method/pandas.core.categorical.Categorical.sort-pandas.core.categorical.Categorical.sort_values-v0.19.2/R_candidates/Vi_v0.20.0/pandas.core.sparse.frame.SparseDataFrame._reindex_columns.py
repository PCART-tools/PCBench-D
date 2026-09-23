    def _reindex_columns(self, columns, method, copy, level, fill_value=None,
                         limit=None, takeable=False):
        if level is not None:
            raise TypeError('Reindex by level not supported for sparse')

        if notnull(fill_value):
            raise NotImplementedError("'fill_value' argument is not supported")

        if limit:
            raise NotImplementedError("'limit' argument is not supported")

        if method is not None:
            raise NotImplementedError("'method' argument is not supported")

        # TODO: fill value handling
        sdict = dict((k, v) for k, v in compat.iteritems(self) if k in columns)
        return self._constructor(
            sdict, index=self.index, columns=columns,
            default_fill_value=self._default_fill_value).__finalize__(self)
