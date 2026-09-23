    def _format_native_types(self, na_rep="NaN", quoting=None, **kwargs):
        """ actually format my specific types """
        from pandas.io.formats.format import ExtensionArrayFormatter

        return ExtensionArrayFormatter(
            values=self, na_rep=na_rep, justify="all", leading_space=False
        ).get_result()
