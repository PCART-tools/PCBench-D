def _unstack_multiple(data, clocs):
    from pandas.core.groupby import decons_obs_group_ids

    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    clocs = [index._get_level_number(i) for i in clocs]

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    clevels = [index.levels[i] for i in clocs]
    clabels = [index.labels[i] for i in clocs]
    cnames = [index.names[i] for i in clocs]
    rlevels = [index.levels[i] for i in rlocs]
    rlabels = [index.labels[i] for i in rlocs]
    rnames = [index.names[i] for i in rlocs]

    shape = [len(x) for x in clevels]
    group_index = get_group_index(clabels, shape, sort=False, xnull=False)

    comp_ids, obs_ids = _compress_group_index(group_index, sort=False)
    recons_labels = decons_obs_group_ids(comp_ids,
                       obs_ids, shape, clabels, xnull=False)

    dummy_index = MultiIndex(levels=rlevels + [obs_ids],
                             labels=rlabels + [comp_ids],
                             names=rnames + ['__placeholder__'],
                             verify_integrity=False)

    if isinstance(data, Series):
        dummy = Series(data.values, index=dummy_index)
        unstacked = dummy.unstack('__placeholder__')
        new_levels = clevels
        new_names = cnames
        new_labels = recons_labels
    else:
        if isinstance(data.columns, MultiIndex):
            result = data
            for i in range(len(clocs)):
                val = clocs[i]
                result = result.unstack(val)
                clocs = [val if i > val else val - 1 for val in clocs]

            return result

        dummy = DataFrame(data.values, index=dummy_index,
                          columns=data.columns)

        unstacked = dummy.unstack('__placeholder__')
        if isinstance(unstacked, Series):
            unstcols = unstacked.index
        else:
            unstcols = unstacked.columns
        new_levels = [unstcols.levels[0]] + clevels
        new_names = [data.columns.name] + cnames

        new_labels = [unstcols.labels[0]]
        for rec in recons_labels:
            new_labels.append(rec.take(unstcols.labels[-1]))

    new_columns = MultiIndex(levels=new_levels, labels=new_labels,
                             names=new_names, verify_integrity=False)

    if isinstance(unstacked, Series):
        unstacked.index = new_columns
    else:
        unstacked.columns = new_columns

    return unstacked
