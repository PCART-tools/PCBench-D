def groupby_internal_repr():
    pdf = pd.DataFrame({'x': [1, 2, 3, 4, 6, 7, 8, 9, 10],
                        'y': list('abcbabbcda')})
    ddf = dd.from_pandas(pdf, 3)

    gp = pdf.groupby('y')
    dp = ddf.groupby('y')
    assert isinstance(dp, dd.groupby.DataFrameGroupBy)
    assert isinstance(dp._pd, pd.core.groupby.DataFrameGroupBy)
    assert isinstance(dp.obj, dd.DataFrame)
    assert eq(dp.obj, gp.obj)

    gp = pdf.groupby('y')['x']
    dp = ddf.groupby('y')['x']
    assert isinstance(dp, dd.groupby.SeriesGroupBy)
    assert isinstance(dp._pd, pd.core.groupby.SeriesGroupBy)
    # slicing should not affect to internal
    assert isinstance(dp.obj, dd.Series)
    assert eq(dp.obj, gp.obj)

    gp = pdf.groupby('y')[['x']]
    dp = ddf.groupby('y')[['x']]
    assert isinstance(dp, dd.groupby.DataFrameGroupBy)
    assert isinstance(dp._pd, pd.core.groupby.DataFrameGroupBy)
    # slicing should not affect to internal
    assert isinstance(dp.obj, dd.DataFrame)
    assert eq(dp.obj, gp.obj)

    gp = pdf.groupby(pdf.y)['x']
    dp = ddf.groupby(ddf.y)['x']
    assert isinstance(dp, dd.groupby.SeriesGroupBy)
    assert isinstance(dp._pd, pd.core.groupby.SeriesGroupBy)
    # slicing should not affect to internal
    assert isinstance(dp.obj, dd.Series)
    assert eq(dp.obj, gp.obj)

    gp = pdf.groupby(pdf.y)[['x']]
    dp = ddf.groupby(ddf.y)[['x']]
    assert isinstance(dp, dd.groupby.DataFrameGroupBy)
    assert isinstance(dp._pd, pd.core.groupby.DataFrameGroupBy)
    # slicing should not affect to internal
    assert isinstance(dp.obj, dd.DataFrame)
    assert eq(dp.obj, gp.obj)
