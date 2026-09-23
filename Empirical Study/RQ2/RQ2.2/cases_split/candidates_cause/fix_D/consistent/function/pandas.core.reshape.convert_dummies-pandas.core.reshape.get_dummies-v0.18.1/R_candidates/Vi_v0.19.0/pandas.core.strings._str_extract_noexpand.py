def _str_extract_noexpand(arr, pat, flags=0):
    """
    Find groups in each string in the Series using passed regular
    expression. This function is called from
    str_extract(expand=False), and can return Series, DataFrame, or
    Index.

    """
    from pandas import DataFrame, Index

    regex = re.compile(pat, flags=flags)
    groups_or_na = _groups_or_na_fun(regex)

    if regex.groups == 1:
        result = np.array([groups_or_na(val)[0] for val in arr], dtype=object)
        name = _get_single_group_name(regex)
    else:
        if isinstance(arr, Index):
            raise ValueError("only one regex group is supported with Index")
        name = None
        names = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
        columns = [names.get(1 + i, i) for i in range(regex.groups)]
        if arr.empty:
            result = DataFrame(columns=columns, dtype=object)
        else:
            result = DataFrame(
                [groups_or_na(val) for val in arr],
                columns=columns,
                index=arr.index,
                dtype=object)
    return result, name
