    def _setitem_array(self, key, value):
        # also raises Exception if object array with NA values
        if com.is_bool_indexer(key):
            # bool indexer is indexing along rows
            if len(key) != len(self.index):
                raise ValueError(
                    f"Item wrong length {len(key)} instead of {len(self.index)}!"
                )
            key = check_bool_indexer(self.index, key)
            indexer = key.nonzero()[0]
            self._check_setitem_copy()
            if isinstance(value, DataFrame):
                # GH#39931 reindex since iloc does not align
                value = value.reindex(self.index.take(indexer))
            self.iloc[indexer] = value

        else:
            # Note: unlike self.iloc[:, indexer] = value, this will
            #  never try to overwrite values inplace

            if isinstance(value, DataFrame):
                check_key_length(self.columns, key, value)
                for k1, k2 in zip(key, value.columns):
                    self[k1] = value[k2]

            elif not is_list_like(value):
                for col in key:
                    self[col] = value

            elif isinstance(value, np.ndarray) and value.ndim == 2:
                self._iset_not_inplace(key, value)

            elif np.ndim(value) > 1:
                # list of lists
                value = DataFrame(value).values
                return self._setitem_array(key, value)

            else:
                self._iset_not_inplace(key, value)
