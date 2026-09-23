def text_blocks_to_pandas(reader, block_lists, header, head, kwargs,
                          collection=True, enforce=False):
    """ Convert blocks of bytes to a dask.dataframe or other high-level object

    This accepts a list of lists of values of bytes where each list corresponds
    to one file, and the value of bytes concatenate to comprise the entire
    file, in order.

    Parameters
    ----------
    reader : callable
        ``pd.read_csv`` or ``pd.read_table``.
    block_lists : list of lists of delayed values of bytes
        The lists of bytestrings where each list corresponds to one logical file
    header : bytestring
        The header, found at the front of the first file, to be prepended to
        all blocks
    head : pd.DataFrame
        An example Pandas DataFrame to be used for metadata.
        Can be ``None`` if ``collection==False``
    kwargs : dict
        Keyword arguments to pass down to ``reader``
    collection: boolean, optional (defaults to True)

    Returns
    -------
    A dask.dataframe or list of delayed values
    """
    dtypes = head.dtypes.to_dict()
    columns = list(head.columns)
    delayed_pandas_read_text = delayed(pandas_read_text)
    dfs = []
    for blocks in block_lists:
        if not blocks:
            continue
        df = delayed_pandas_read_text(reader, blocks[0], header, kwargs,
                                      dtypes, columns, write_header=False,
                                      enforce=enforce)
        dfs.append(df)
        for b in blocks[1:]:
            dfs.append(delayed_pandas_read_text(reader, b, header, kwargs,
                                                dtypes, columns,
                                                enforce=enforce))

    if collection:
        head = clear_known_categories(head)
        return from_delayed(dfs, head)
    else:
        return dfs
