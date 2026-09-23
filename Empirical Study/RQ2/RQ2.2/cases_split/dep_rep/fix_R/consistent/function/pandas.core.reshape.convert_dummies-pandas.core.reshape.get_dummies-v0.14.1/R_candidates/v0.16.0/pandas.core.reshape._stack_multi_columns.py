def _stack_multi_columns(frame, level_num=-1, dropna=True):
    def _convert_level_number(level_num, columns):
        """
        Logic for converting the level number to something
        we can safely pass to swaplevel:

        We generally want to convert the level number into
        a level name, except when columns do not have names,
        in which case we must leave as a level number
        """
        if level_num in columns.names:
            return columns.names[level_num]
        else:
            if columns.names[level_num] is None:
                return level_num
            else:
                return columns.names[level_num]

    this = frame.copy()

    # this makes life much simpler
    if level_num != frame.columns.nlevels - 1:
        # roll levels to put selected level at end
        roll_columns = this.columns
        for i in range(level_num, frame.columns.nlevels - 1):
            # Need to check if the ints conflict with level names
            lev1 = _convert_level_number(i, roll_columns)
            lev2 = _convert_level_number(i + 1, roll_columns)
            roll_columns = roll_columns.swaplevel(lev1, lev2)
        this.columns = roll_columns

    if not this.columns.is_lexsorted():
        # Workaround the edge case where 0 is one of the column names,
        # which interferes with trying to sort based on the first
        # level
        level_to_sort = _convert_level_number(0, this.columns)
        this = this.sortlevel(level_to_sort, axis=1)

    # tuple list excluding level for grouping columns
    if len(frame.columns.levels) > 2:
        tuples = list(zip(*[
            lev.take(lab) for lev, lab in
            zip(this.columns.levels[:-1], this.columns.labels[:-1])
        ]))
        unique_groups = [key for key, _ in itertools.groupby(tuples)]
        new_names = this.columns.names[:-1]
        new_columns = MultiIndex.from_tuples(unique_groups, names=new_names)
    else:
        new_columns = unique_groups = this.columns.levels[0]

    # time to ravel the values
    new_data = {}
    level_vals = this.columns.levels[-1]
    level_labels = sorted(set(this.columns.labels[-1]))
    level_vals_used = level_vals[level_labels]
    levsize = len(level_labels)
    drop_cols = []
    for key in unique_groups:
        loc = this.columns.get_loc(key)
        slice_len = loc.stop - loc.start
        # can make more efficient?

        if slice_len == 0:
            drop_cols.append(key)
            continue
        elif slice_len != levsize:
            chunk = this.ix[:, this.columns[loc]]
            chunk.columns = level_vals.take(chunk.columns.labels[-1])
            value_slice = chunk.reindex(columns=level_vals_used).values
        else:
            if frame._is_mixed_type:
                value_slice = this.ix[:, this.columns[loc]].values
            else:
                value_slice = this.values[:, loc]

        new_data[key] = value_slice.ravel()

    if len(drop_cols) > 0:
        new_columns = new_columns - drop_cols

    N = len(this)

    if isinstance(this.index, MultiIndex):
        new_levels = list(this.index.levels)
        new_names = list(this.index.names)
        new_labels = [lab.repeat(levsize) for lab in this.index.labels]
    else:
        new_levels = [this.index]
        new_labels = [np.arange(N).repeat(levsize)]
        new_names = [this.index.name]  # something better?

    new_levels.append(frame.columns.levels[level_num])
    new_labels.append(np.tile(level_labels, N))
    new_names.append(frame.columns.names[level_num])

    new_index = MultiIndex(levels=new_levels, labels=new_labels,
                           names=new_names, verify_integrity=False)

    result = DataFrame(new_data, index=new_index, columns=new_columns)

    # more efficient way to go about this? can do the whole masking biz but
    # will only save a small amount of time...
    if dropna:
        result = result.dropna(axis=0, how='all')

    return result
