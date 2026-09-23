def value_counts_combine(x):
    return x.groupby(level=0).sum()
