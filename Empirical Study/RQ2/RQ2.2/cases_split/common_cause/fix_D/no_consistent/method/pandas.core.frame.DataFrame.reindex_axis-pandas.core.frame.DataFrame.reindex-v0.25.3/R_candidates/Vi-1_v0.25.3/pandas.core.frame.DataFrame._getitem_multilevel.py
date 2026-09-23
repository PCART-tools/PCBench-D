    def _getitem_multilevel(self, key):
        loc = self.columns.get_loc(key)
        if isinstance(loc, (slice, Series, np.ndarray, Index)):
            new_columns = self.columns[loc]
            result_columns = maybe_droplevels(new_columns, key)
            if self._is_mixed_type:
                result = self.reindex(columns=new_columns)
                result.columns = result_columns
            else:
                new_values = self.values[:, loc]
                result = self._constructor(
                    new_values, index=self.index, columns=result_columns
                )
                result = result.__finalize__(self)

            # If there is only one column being returned, and its name is
            # either an empty string, or a tuple with an empty string as its
            # first element, then treat the empty string as a placeholder
            # and return the column as if the user had provided that empty
            # string in the key. If the result is a Series, exclude the
            # implied empty string from its name.
            if len(result.columns) == 1:
                top = result.columns[0]
                if isinstance(top, tuple):
                    top = top[0]
                if top == "":
                    result = result[""]
                    if isinstance(result, Series):
                        result = self._constructor_sliced(
                            result, index=self.index, name=key
                        )

            result._set_is_copy(self)
            return result
        else:
            return self._get_item_cache(key)
