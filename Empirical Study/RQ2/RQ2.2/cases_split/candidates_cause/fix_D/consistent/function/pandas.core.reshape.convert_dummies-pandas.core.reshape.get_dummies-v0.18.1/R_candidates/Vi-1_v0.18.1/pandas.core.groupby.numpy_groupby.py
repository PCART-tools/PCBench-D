def numpy_groupby(data, labels, axis=0):
    s = np.argsort(labels)
    keys, inv = np.unique(labels, return_inverse=True)
    i = inv.take(s)
    groups_at = np.where(i != np.concatenate(([-1], i[:-1])))[0]
    ordered_data = data.take(s, axis=axis)
    group_sums = np.add.reduceat(ordered_data, groups_at, axis=axis)

    return group_sums
