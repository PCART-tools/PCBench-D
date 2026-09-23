    def __getitem__(self, key):

        # shortcut if we are an actual column
        is_mi_columns = isinstance(self.columns, MultiIndex)
        try:
            if key in self.columns and not is_mi_columns:
                return self._getitem_column(key)
        except:
            pass

        # see if we can slice the rows
        indexer = _convert_to_index_sliceable(self, key)
        if indexer is not None:
            return self._getitem_slice(indexer)

        if isinstance(key, (Series, np.ndarray, list)):
            # either boolean or fancy integer index
            return self._getitem_array(key)
        elif isinstance(key, DataFrame):
            return self._getitem_frame(key)
        elif is_mi_columns:
            return self._getitem_multilevel(key)
        else:
            return self._getitem_column(key)
