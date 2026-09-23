def test_series_format_long():
    s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10,
                  index=list('ABCDEFGHIJ') * 10)
    ds = dd.from_pandas(s, 10)
    exp = ("Dask Series Structure:\nnpartitions=10\nA    int64\nB      ...\n"
           "     ...  \nJ      ...\nJ      ...\ndtype: int64\n"
           "Dask Name: from_pandas, 10 tasks")
    assert repr(ds) == exp
    assert str(ds) == exp

    exp = "npartitions=10\nA    int64\nB      ...\n     ...  \nJ      ...\nJ      ..."
    assert ds.to_string() == exp
