    @Appender(_shared_docs['unique'] % _indexops_doc_kwargs)
    def unique(self):
        values = self._values

        if hasattr(values, 'unique'):
            result = values.unique()
        else:
            from pandas.core.nanops import unique1d
            result = unique1d(values)
        return result
