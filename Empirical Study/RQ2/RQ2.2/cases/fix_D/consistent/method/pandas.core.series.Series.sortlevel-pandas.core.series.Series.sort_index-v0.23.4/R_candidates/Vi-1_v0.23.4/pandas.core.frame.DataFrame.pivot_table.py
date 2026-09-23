    @Substitution('')
    @Appender(_shared_docs['pivot_table'])
    def pivot_table(self, values=None, index=None, columns=None,
                    aggfunc='mean', fill_value=None, margins=False,
                    dropna=True, margins_name='All'):
        from pandas.core.reshape.pivot import pivot_table
        return pivot_table(self, values=values, index=index, columns=columns,
                           aggfunc=aggfunc, fill_value=fill_value,
                           margins=margins, dropna=dropna,
                           margins_name=margins_name)
