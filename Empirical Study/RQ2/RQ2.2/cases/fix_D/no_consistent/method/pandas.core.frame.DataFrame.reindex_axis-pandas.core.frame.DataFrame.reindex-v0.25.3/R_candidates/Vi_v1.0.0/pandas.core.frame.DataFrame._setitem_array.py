    def _setitem_array(self, key, value):
        # also raises Exception if object array with NA values
        if com.is_bool_indexer(key):
            if len(key) != len(self.index):
                raise ValueError(
                    f"Item wrong length {len(key)} instead of {len(self.index)}!"
                )
            key = check_bool_indexer(self.index, key)
            indexer = key.nonzero()[0]
            self._check_setitem_copy()
            self.loc._setitem_with_indexer(indexer, value)
        else:
            if isinstance(value, DataFrame):
                if len(value.columns) != len(key):
                    raise ValueError("Columns must be same length as key")
                for k1, k2 in zip(key, value.columns):
                    self[k1] = value[k2]
            else:
                indexer = self.loc._get_listlike_indexer(
                    key, axis=1, raise_missing=False
                )[1]
                self._check_setitem_copy()
                self.loc._setitem_with_indexer((slice(None), indexer), value)
