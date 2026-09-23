def set_partitions_pre(s, divisions):
    partitions = pd.Series(divisions).searchsorted(s, side='right') - 1
    partitions[(s >= divisions[-1]).values] = len(divisions) - 2
    return partitions
