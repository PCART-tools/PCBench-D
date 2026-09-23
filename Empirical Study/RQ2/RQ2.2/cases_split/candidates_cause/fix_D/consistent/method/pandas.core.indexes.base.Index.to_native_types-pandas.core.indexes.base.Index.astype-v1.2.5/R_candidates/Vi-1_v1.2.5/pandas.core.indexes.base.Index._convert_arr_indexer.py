    def _convert_arr_indexer(self, keyarr):
        """
        Convert an array-like indexer to the appropriate dtype.

        Parameters
        ----------
        keyarr : array-like
            Indexer to convert.

        Returns
        -------
        converted_keyarr : array-like
        """
        keyarr = com.asarray_tuplesafe(keyarr)
        return keyarr
