    @Appender(_index_shared_docs['_convert_list_indexer'])
    def _convert_list_indexer(self, keyarr, kind=None):
        if (kind in [None, 'iloc', 'ix'] and
                is_integer_dtype(keyarr) and not self.is_floating() and
                not isinstance(keyarr, ABCPeriodIndex)):

            if self.inferred_type == 'mixed-integer':
                indexer = self.get_indexer(keyarr)
                if (indexer >= 0).all():
                    return indexer
                # missing values are flagged as -1 by get_indexer and negative
                # indices are already converted to positive indices in the
                # above if-statement, so the negative flags are changed to
                # values outside the range of indices so as to trigger an
                # IndexError in maybe_convert_indices
                indexer[indexer < 0] = len(self)
                from pandas.core.indexing import maybe_convert_indices
                return maybe_convert_indices(indexer, len(self))

            elif not self.inferred_type == 'integer':
                keyarr = np.where(keyarr < 0, len(self) + keyarr, keyarr)
                return keyarr

        return None
