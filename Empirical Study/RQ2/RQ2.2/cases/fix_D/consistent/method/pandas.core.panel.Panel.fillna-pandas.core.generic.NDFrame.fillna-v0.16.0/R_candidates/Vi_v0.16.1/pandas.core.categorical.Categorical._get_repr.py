    def _get_repr(self, name=False, length=True, na_rep='NaN', footer=True):
        from pandas.core import format as fmt
        formatter = fmt.CategoricalFormatter(self,
                                             name=name,
                                             length=length,
                                             na_rep=na_rep,
                                             footer=footer)
        result = formatter.to_string()
        return compat.text_type(result)
