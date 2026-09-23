def test_gh3579():
    assert_eq(np.arange(10)[0::-1], da.arange(10, chunks=3)[0::-1])
    assert_eq(np.arange(10)[::-1], da.arange(10, chunks=3)[::-1])
