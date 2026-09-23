def test_loc_with_series():
    assert_eq(d.loc[d.a % 2 == 0], full.loc[full.a % 2 == 0])

    assert sorted(d.loc[d.a % 2].dask) == sorted(d.loc[d.a % 2].dask)
    assert sorted(d.loc[d.a % 2].dask) != sorted(d.loc[d.a % 3].dask)
