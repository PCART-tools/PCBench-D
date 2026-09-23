def test_raise_informative_errors_no_chunks():
    X = np.arange(10)
    a = da.from_array(X, chunks=(5, 5))
    a._chunks = ((np.nan, np.nan),)

    b = da.from_array(X, chunks=(4, 4, 2))
    b._chunks = ((np.nan, np.nan, np.nan),)

    for op in [lambda: a + b,
               lambda: a[1],
               lambda: a[::2],
               lambda: a[-5],
               lambda: a.rechunk(3),
               lambda: a.reshape(2, 5)]:
        with pytest.raises(ValueError) as e:
            op()
        if 'chunk' not in str(e) or 'unknown' not in str(e):
            op()
