    @doc(Index._convert_arr_indexer)
    def _convert_arr_indexer(self, keyarr):
        try:
            return self._data._validate_listlike(keyarr, allow_object=True)
        except (ValueError, TypeError):
            return com.asarray_tuplesafe(keyarr)
