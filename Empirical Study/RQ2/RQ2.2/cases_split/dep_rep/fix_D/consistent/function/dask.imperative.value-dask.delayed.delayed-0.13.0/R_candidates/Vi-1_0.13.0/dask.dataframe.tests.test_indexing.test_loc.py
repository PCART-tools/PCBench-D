def test_loc():
    assert d.loc[3:8].divisions[0] == 3
    assert d.loc[3:8].divisions[-1] == 8

    assert d.loc[5].divisions == (5, 5)

    assert_eq(d.loc[5], full.loc[5:5])
    assert_eq(d.loc[3:8], full.loc[3:8])
    assert_eq(d.loc[:8], full.loc[:8])
    assert_eq(d.loc[3:], full.loc[3:])

    assert_eq(d.a.loc[5], full.a.loc[5:5])
    assert_eq(d.a.loc[3:8], full.a.loc[3:8])
    assert_eq(d.a.loc[:8], full.a.loc[:8])
    assert_eq(d.a.loc[3:], full.a.loc[3:])

    pytest.raises(KeyError, lambda: d.loc[1000])
    assert_eq(d.loc[1000:], full.loc[1000:])
    assert_eq(d.loc[-2000:-1000], full.loc[-2000:-1000])

    assert sorted(d.loc[5].dask) == sorted(d.loc[5].dask)
    assert sorted(d.loc[5].dask) != sorted(d.loc[6].dask)
