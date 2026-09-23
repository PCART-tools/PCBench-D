def test_no_chunks():
    X = np.arange(11)
    dsk = {('x', 0): np.arange(5), ('x', 1): np.arange(5, 11)}
    x = Array(dsk, 'x', ((np.nan, np.nan,),), np.arange(1).dtype)
    assert_eq(x + 1, X + 1)
    assert_eq(x.sum(), X.sum())
    assert_eq((x + 1).std(), (X + 1).std())
    assert_eq((x + x).std(), (X + X).std())
    assert_eq((x + x).std(keepdims=True), (X + X).std(keepdims=True))
