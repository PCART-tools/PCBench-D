def shuffle_group_3(df, col, npartitions, p):
    g = df.groupby(col)
    d = {i: g.get_group(i) for i in g.groups}
    p.append(d, fsync=True)
