def value_counts_aggregate(x):
    return x.groupby(level=0).sum().sort_values(ascending=False)
