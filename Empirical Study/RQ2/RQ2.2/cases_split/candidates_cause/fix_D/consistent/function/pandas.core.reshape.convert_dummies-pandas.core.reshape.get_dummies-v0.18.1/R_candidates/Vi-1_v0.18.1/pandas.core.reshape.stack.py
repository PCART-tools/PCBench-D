def stack(frame, level=-1, dropna=True):
    """
    Convert DataFrame to Series with multi-level Index. Columns become the
    second level of the resulting hierarchical index

    Returns
    -------
    stacked : Series
    """

    def factorize(index):
        if index.is_unique:
            return index, np.arange(len(index))
        cat = Categorical(index, ordered=True)
        return cat.categories, cat.codes

    N, K = frame.shape
    if isinstance(frame.columns, MultiIndex):
        if frame.columns._reference_duplicate_name(level):
            msg = ("Ambiguous reference to {0}. The column "
                   "names are not unique.".format(level))
            raise ValueError(msg)

    # Will also convert negative level numbers and check if out of bounds.
    level_num = frame.columns._get_level_number(level)

    if isinstance(frame.columns, MultiIndex):
        return _stack_multi_columns(frame, level_num=level_num, dropna=dropna)
    elif isinstance(frame.index, MultiIndex):
        new_levels = list(frame.index.levels)
        new_labels = [lab.repeat(K) for lab in frame.index.labels]

        clev, clab = factorize(frame.columns)
        new_levels.append(clev)
        new_labels.append(np.tile(clab, N).ravel())

        new_names = list(frame.index.names)
        new_names.append(frame.columns.name)
        new_index = MultiIndex(levels=new_levels, labels=new_labels,
                               names=new_names, verify_integrity=False)
    else:
        levels, (ilab, clab) = zip(*map(factorize, (frame.index,
                                                    frame.columns)))
        labels = ilab.repeat(K), np.tile(clab, N).ravel()
        new_index = MultiIndex(levels=levels, labels=labels,
                               names=[frame.index.name, frame.columns.name],
                               verify_integrity=False)

    new_values = frame.values.ravel()
    if dropna:
        mask = notnull(new_values)
        new_values = new_values[mask]
        new_index = new_index[mask]
    return Series(new_values, index=new_index)
