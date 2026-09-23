    def _setitem_with_indexer_missing(self, indexer, value):
        """
        Insert new row(s) or column(s) into the Series or DataFrame.
        """
        from pandas import Series

        # reindex the axis to the new value
        # and set inplace
        if self.ndim == 1:
            index = self.obj.index
            new_index = index.insert(len(index), indexer)

            # we have a coerced indexer, e.g. a float
            # that matches in an Int64Index, so
            # we will not create a duplicate index, rather
            # index to that element
            # e.g. 0.0 -> 0
            # GH#12246
            if index.is_unique:
                new_indexer = index.get_indexer([new_index[-1]])
                if (new_indexer != -1).any():
                    return self._setitem_with_indexer(new_indexer, value)

            # this preserves dtype of the value
            new_values = Series([value])._values
            if len(self.obj._values):
                # GH#22717 handle casting compatibility that np.concatenate
                #  does incorrectly
                new_values = concat_compat([self.obj._values, new_values])
            self.obj._data = self.obj._constructor(
                new_values, index=new_index, name=self.obj.name
            )._data
            self.obj._maybe_update_cacher(clear=True)
            return self.obj

        elif self.ndim == 2:

            if not len(self.obj.columns):
                # no columns and scalar
                raise ValueError("cannot set a frame with no defined columns")

            if isinstance(value, ABCSeries):
                # append a Series
                value = value.reindex(index=self.obj.columns, copy=True)
                value.name = indexer

            else:
                # a list-list
                if is_list_like_indexer(value):
                    # must have conforming columns
                    if len(value) != len(self.obj.columns):
                        raise ValueError("cannot set a row with mismatched columns")

                value = Series(value, index=self.obj.columns, name=indexer)

            self.obj._data = self.obj.append(value)._data
            self.obj._maybe_update_cacher(clear=True)
            return self.obj
