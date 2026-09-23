    def _get_repr(self, length=True, na_rep='NaN', footer=True):
        from pandas.io.formats import format as fmt
        formatter = fmt.CategoricalFormatter(self, length=length,
                                             na_rep=na_rep, footer=footer)
        result = formatter.to_string()
        return compat.text_type(result)
