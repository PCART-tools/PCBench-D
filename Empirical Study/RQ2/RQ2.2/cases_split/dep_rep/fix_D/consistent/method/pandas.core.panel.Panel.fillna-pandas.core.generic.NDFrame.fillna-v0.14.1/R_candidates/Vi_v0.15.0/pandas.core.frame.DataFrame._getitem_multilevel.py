    def _getitem_multilevel(self, key):
        loc = self.columns.get_loc(key)
        if isinstance(loc, (slice, Series, np.ndarray, Index)):
            new_columns = self.columns[loc]
            result_columns = _maybe_droplevels(new_columns, key)
            if self._is_mixed_type:
                result = self.reindex(columns=new_columns)
                result.columns = result_columns
            else:
                new_values = self.values[:, loc]
                result = DataFrame(new_values, index=self.index,
                                   columns=result_columns).__finalize__(self)
            if len(result.columns) == 1:
                top = result.columns[0]
                if ((type(top) == str and top == '') or
                        (type(top) == tuple and top[0] == '')):
                    result = result['']
                    if isinstance(result, Series):
                        result = Series(result, index=self.index, name=key)

            result._set_is_copy(self)
            return result
        else:
            return self._get_item_cache(key)
