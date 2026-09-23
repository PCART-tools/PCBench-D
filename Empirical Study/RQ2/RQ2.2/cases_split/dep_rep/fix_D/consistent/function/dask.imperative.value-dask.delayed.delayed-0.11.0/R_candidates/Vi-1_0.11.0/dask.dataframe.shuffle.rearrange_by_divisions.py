def rearrange_by_divisions(df, column, divisions, max_branch=None, shuffle=None):
    """ Shuffle dataframe so that column separates along divisions """
    partitions = df[column].map_partitions(set_partitions_pre,
                divisions=divisions, meta=pd.Series([0]))
    df2 = df.assign(_partitions=partitions)
    df3 = rearrange_by_column(df2, '_partitions', max_branch=max_branch,
                              npartitions=len(divisions) - 1, shuffle=shuffle)
    return df3.drop('_partitions', axis=1, dtype=df.columns.dtype)
