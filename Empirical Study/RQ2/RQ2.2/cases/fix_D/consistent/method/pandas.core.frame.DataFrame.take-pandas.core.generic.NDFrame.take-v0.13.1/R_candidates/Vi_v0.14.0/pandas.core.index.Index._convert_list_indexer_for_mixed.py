    def _convert_list_indexer_for_mixed(self, keyarr, typ=None):
        """ passed a key that is tuplesafe that is integer based
            and we have a mixed index (e.g. number/labels). figure out
            the indexer. return None if we can't help
        """
        if com.is_integer_dtype(keyarr) and not self.is_floating():
            if self.inferred_type != 'integer':
                keyarr = np.where(keyarr < 0,
                                  len(self) + keyarr, keyarr)

            if self.inferred_type == 'mixed-integer':
                indexer = self.get_indexer(keyarr)
                if (indexer >= 0).all():
                    return indexer

                from pandas.core.indexing import _maybe_convert_indices
                return _maybe_convert_indices(indexer, len(self))

            elif not self.inferred_type == 'integer':
                return keyarr

        return None
