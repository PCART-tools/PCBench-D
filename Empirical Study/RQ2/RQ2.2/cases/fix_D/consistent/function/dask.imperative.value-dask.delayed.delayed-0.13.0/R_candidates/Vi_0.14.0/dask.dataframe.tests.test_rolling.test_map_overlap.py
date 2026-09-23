@pytest.mark.parametrize('npartitions', [1, 4])
def test_map_overlap(npartitions):
    ddf = dd.from_pandas(df, npartitions)
    for before, after in [(0, 3), (3, 0), (3, 3), (0, 0)]:
        # DataFrame
        res = ddf.map_overlap(shifted_sum, before, after, before, after, c=2)
        sol = shifted_sum(df, before, after, c=2)
        assert_eq(res, sol)

        # Series
        res = ddf.b.map_overlap(shifted_sum, before, after, before, after, c=2)
        sol = shifted_sum(df.b, before, after, c=2)
        assert_eq(res, sol)
