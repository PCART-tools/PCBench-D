    def _setitem_array(self, key, value):
        # also raises Exception if object array with NA values
        if com._is_bool_indexer(key):
            if len(key) != len(self.index):
                raise ValueError('Item wrong length %d instead of %d!' %
                                 (len(key), len(self.index)))
            key = _check_bool_indexer(self.index, key)
            indexer = key.nonzero()[0]
            self.ix._setitem_with_indexer(indexer, value)
        else:
            if isinstance(value, DataFrame):
                if len(value.columns) != len(key):
                    raise ValueError('Columns must be same length as key')
                for k1, k2 in zip(key, value.columns):
                    self[k1] = value[k2]
            else:
                indexer = self.ix._convert_to_indexer(key, axis=1)
                self.ix._setitem_with_indexer((slice(None), indexer), value)
