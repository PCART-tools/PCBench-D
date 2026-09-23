    def _format_native_types(self, na_rep='', quoting=None, **kwargs):
        """ actually format my specific types """
        from pandas.io.formats.format import IntervalArrayFormatter
        return IntervalArrayFormatter(values=self,
                                      na_rep=na_rep,
                                      justify='all').get_result()
