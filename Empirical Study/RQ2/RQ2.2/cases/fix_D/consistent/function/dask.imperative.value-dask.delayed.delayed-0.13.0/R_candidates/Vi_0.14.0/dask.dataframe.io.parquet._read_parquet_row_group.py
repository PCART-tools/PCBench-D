def _read_parquet_row_group(open, fn, index, columns, rg, series, categories,
                            helper, cs, dt, *args):
    if not isinstance(columns, (tuple, list)):
        columns = (columns,)
        series = True
    if index and index not in columns:
        columns = columns + type(columns)([index])
    df, views = _pre_allocate(rg.num_rows, columns, categories, index, cs, dt)
    read_row_group_file(fn, rg, columns, categories, helper, cs,
                        open=open, assign=views)

    if series:
        return df[df.columns[0]]
    else:
        return df
