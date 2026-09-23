def groupby_internal_head():
    pdf = pd.DataFrame({'A': [1, 2] * 10,
                        'B': np.random.randn(20),
                        'C': np.random.randn(20)})
    ddf = dd.from_pandas(pdf, 3)

    assert eq(ddf.groupby('A')._head().sum(),
              pdf.head().groupby('A').sum())

    assert eq(ddf.groupby(ddf['A'])._head().sum(),
              pdf.head().groupby(pdf['A']).sum())

    assert eq(ddf.groupby(ddf['A'] + 1)._head().sum(),
              pdf.head().groupby(pdf['A'] + 1).sum())
