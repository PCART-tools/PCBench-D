def load_castra_partition(castra, part, columns, index):
    import blosc
    # Due to serialization issues, blosc needs to be manually initialized in
    # each process.
    blosc.init()

    df = castra.load_partition(part, columns)
    if isinstance(columns, list):
        items = df.itertuples(index)
    else:
        items = df.iteritems() if index else iter(df)

    items = list(items)
    if items and isinstance(items[0], tuple) and type(items[0]) is not tuple:
        names = items[0]._fields
        items = [dict(zip(names, item)) for item in items]

    return items
