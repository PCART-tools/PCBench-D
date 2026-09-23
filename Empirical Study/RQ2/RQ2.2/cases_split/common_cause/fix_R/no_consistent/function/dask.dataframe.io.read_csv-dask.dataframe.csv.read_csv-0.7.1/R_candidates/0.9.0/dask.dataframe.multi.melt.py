def melt(frame, id_vars=None, value_vars=None, var_name=None,
         value_name='value', col_level=None):

    from dask.dataframe.core import no_default

    return frame.map_partitions(pd.melt, no_default, id_vars=id_vars,
                                value_vars=value_vars,
                                var_name=var_name, value_name=value_name,
                                col_level=col_level, token='melt')
