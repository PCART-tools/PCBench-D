def _groupby_raise_unaligned(df, **kwargs):
    """Groupby, but raise if df and `by` key are unaligned.

    Pandas supports grouping by a column that doesn't align with the input
    frame/series/index. However, the reindexing this causes doesn't seem to be
    threadsafe, and can result in incorrect results. Since grouping by an
    unaligned key is generally a bad idea, we just error loudly in dask.

    For more information see pandas GH issue #15244 and Dask GH issue #1876."""
    by = kwargs.get('by', None)
    if by is not None and not _is_aligned(df, by):
        msg = ("Grouping by an unaligned index is unsafe and unsupported.\n"
               "This can be caused by filtering only one of the object or\n"
               "grouping key. For example, the following works in pandas,\n"
               "but not in dask:\n"
               "\n"
               "df[df.foo < 0].groupby(df.bar)\n"
               "\n"
               "This can be avoided by either filtering beforehand, or\n"
               "passing in the name of the column instead:\n"
               "\n"
               "df2 = df[df.foo < 0]\n"
               "df2.groupby(df2.bar)\n"
               "# or\n"
               "df[df.foo < 0].groupby('bar')\n"
               "\n"
               "For more information see dask GH issue #1876.")
        raise ValueError(msg)
    return df.groupby(**kwargs)
