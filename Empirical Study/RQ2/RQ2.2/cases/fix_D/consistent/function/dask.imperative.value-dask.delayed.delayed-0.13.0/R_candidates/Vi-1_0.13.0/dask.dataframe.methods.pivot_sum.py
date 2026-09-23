def pivot_sum(df, index, columns, values):
    return pd.pivot_table(df, index=index, columns=columns,
                          values=values, aggfunc='sum')
