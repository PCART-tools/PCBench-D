    def take(self, indexer, allow_fill=False, fill_value=None):
        from pandas.api.extensions import take

        # we always fill with 1 internally
        # to avoid upcasting
        data_fill_value = 1 if isna(fill_value) else fill_value
        result = take(self._data, indexer, fill_value=data_fill_value,
                      allow_fill=allow_fill)

        mask = take(self._mask, indexer, fill_value=True,
                    allow_fill=allow_fill)

        # if we are filling
        # we only fill where the indexer is null
        # not existing missing values
        # TODO(jreback) what if we have a non-na float as a fill value?
        if allow_fill and notna(fill_value):
            fill_mask = np.asarray(indexer) == -1
            result[fill_mask] = fill_value
            mask = mask ^ fill_mask

        return type(self)(result, mask, copy=False)
