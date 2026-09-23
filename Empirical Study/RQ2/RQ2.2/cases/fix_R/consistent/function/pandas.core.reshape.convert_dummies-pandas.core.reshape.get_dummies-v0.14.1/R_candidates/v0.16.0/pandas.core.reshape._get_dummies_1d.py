def _get_dummies_1d(data, prefix, prefix_sep='_', dummy_na=False):
    # Series avoids inconsistent NaN handling
    cat = Categorical.from_array(Series(data), ordered=True)
    levels = cat.categories

    # if all NaN
    if not dummy_na and len(levels) == 0:
        if isinstance(data, Series):
            index = data.index
        else:
            index = np.arange(len(data))
        return DataFrame(index=index)

    number_of_cols = len(levels)
    if dummy_na:
        number_of_cols += 1

    dummy_mat = np.eye(number_of_cols).take(cat.codes, axis=0)

    if dummy_na:
        levels = np.append(cat.categories, np.nan)
    else:
        # reset NaN GH4446
        dummy_mat[cat.codes == -1] = 0

    if prefix is not None:
        dummy_cols = ['%s%s%s' % (prefix, prefix_sep, v)
                      for v in levels]
    else:
        dummy_cols = levels

    if isinstance(data, Series):
        index = data.index
    else:
        index = None

    return DataFrame(dummy_mat, index=index, columns=dummy_cols)
