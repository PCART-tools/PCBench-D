def test_apply_shuffle():
    pdf = pd.DataFrame({'A': [1, 2, 3, 4] * 5,
                        'B': np.random.randn(20),
                        'C': np.random.randn(20),
                        'D': np.random.randn(20)})
    ddf = dd.from_pandas(pdf, 3)

    assert eq(ddf.groupby('A').apply(lambda x: x.sum()),
              pdf.groupby('A').apply(lambda x: x.sum()))

    assert eq(ddf.groupby(ddf['A']).apply(lambda x: x.sum()),
              pdf.groupby(pdf['A']).apply(lambda x: x.sum()))

    assert eq(ddf.groupby(ddf['A'] + 1).apply(lambda x: x.sum()),
              pdf.groupby(pdf['A'] + 1).apply(lambda x: x.sum()))

    # SeriesGroupBy
    assert eq(ddf.groupby('A')['B'].apply(lambda x: x.sum()),
              pdf.groupby('A')['B'].apply(lambda x: x.sum()))

    assert eq(ddf.groupby(ddf['A'])['B'].apply(lambda x: x.sum()),
              pdf.groupby(pdf['A'])['B'].apply(lambda x: x.sum()))

    assert eq(ddf.groupby(ddf['A'] + 1)['B'].apply(lambda x: x.sum()),
              pdf.groupby(pdf['A'] + 1)['B'].apply(lambda x: x.sum()))

    # DataFrameGroupBy with column slice
    assert eq(ddf.groupby('A')[['B', 'C']].apply(lambda x: x.sum()),
              pdf.groupby('A')[['B', 'C']].apply(lambda x: x.sum()))

    assert eq(ddf.groupby(ddf['A'])[['B', 'C']].apply(lambda x: x.sum()),
              pdf.groupby(pdf['A'])[['B', 'C']].apply(lambda x: x.sum()))

    assert eq(ddf.groupby(ddf['A'] + 1)[['B', 'C']].apply(lambda x: x.sum()),
              pdf.groupby(pdf['A'] + 1)[['B', 'C']].apply(lambda x: x.sum()))
