def shuffle_group_2(df, col):
    g = df.groupby(col)
    return {i: g.get_group(i) for i in g.groups}, df.head(0)
