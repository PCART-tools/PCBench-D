    def _format_native_types(self, na_rep=u('NaT'),
                             date_format=None, **kwargs):
        from pandas.io.formats.format import Timedelta64Formatter
        return Timedelta64Formatter(values=self,
                                    nat_rep=na_rep,
                                    justify='all').get_result()
