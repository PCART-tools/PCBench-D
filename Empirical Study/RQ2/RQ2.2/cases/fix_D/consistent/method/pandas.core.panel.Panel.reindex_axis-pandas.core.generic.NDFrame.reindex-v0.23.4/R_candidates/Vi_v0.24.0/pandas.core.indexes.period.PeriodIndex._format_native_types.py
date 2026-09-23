    def _format_native_types(self, na_rep=u'NaT', quoting=None, **kwargs):
        # just dispatch, return ndarray
        return self._data._format_native_types(na_rep=na_rep,
                                               quoting=quoting,
                                               **kwargs)
