@pytest.mark.parametrize('split_every', [False, 2])
def test_allany(split_every):
    df = pd.DataFrame(np.random.choice([True, False], size=(100, 4)),
                      columns=['A', 'B', 'C', 'D'])
    df['E'] = list('abcde') * 20
    ddf = dd.from_pandas(df, 10)

    assert_eq(ddf.all(split_every=split_every), df.all())
    assert_eq(ddf.all(axis=1, split_every=split_every), df.all(axis=1))
    assert_eq(ddf.all(axis=0, split_every=split_every), df.all(axis=0))

    assert_eq(ddf.any(split_every=split_every), df.any())
    assert_eq(ddf.any(axis=1, split_every=split_every), df.any(axis=1))
    assert_eq(ddf.any(axis=0, split_every=split_every), df.any(axis=0))

    assert_eq(ddf.A.all(split_every=split_every), df.A.all())
    assert_eq(ddf.A.any(split_every=split_every), df.A.any())
