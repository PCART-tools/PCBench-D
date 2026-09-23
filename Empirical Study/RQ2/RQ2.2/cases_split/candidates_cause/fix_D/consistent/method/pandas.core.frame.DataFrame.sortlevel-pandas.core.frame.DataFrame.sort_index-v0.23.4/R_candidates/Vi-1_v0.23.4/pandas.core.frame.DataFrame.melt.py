    @Appender(_shared_docs['melt'] %
              dict(caller='df.melt(',
                   versionadded='.. versionadded:: 0.20.0\n',
                   other='melt'))
    def melt(self, id_vars=None, value_vars=None, var_name=None,
             value_name='value', col_level=None):
        from pandas.core.reshape.melt import melt
        return melt(self, id_vars=id_vars, value_vars=value_vars,
                    var_name=var_name, value_name=value_name,
                    col_level=col_level)
