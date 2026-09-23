def test_20news_vectorized():
    try:
        datasets.fetch_20newsgroups(subset='all',
                                    download_if_missing=False)
    except IOError:
        raise SkipTest("Download 20 newsgroups to run this test")

    # test subset = train
    bunch = datasets.fetch_20newsgroups_vectorized(subset="train")
    assert_true(sp.isspmatrix_csr(bunch.data))
    assert_equal(bunch.data.shape, (11314, 130107))
    assert_equal(bunch.target.shape[0], 11314)
    assert_equal(bunch.data.dtype, np.float64)

    # test subset = test
    bunch = datasets.fetch_20newsgroups_vectorized(subset="test")
    assert_true(sp.isspmatrix_csr(bunch.data))
    assert_equal(bunch.data.shape, (7532, 130107))
    assert_equal(bunch.target.shape[0], 7532)
    assert_equal(bunch.data.dtype, np.float64)

    # test return_X_y option
    fetch_func = partial(datasets.fetch_20newsgroups_vectorized, subset='test')
    check_return_X_y(bunch, fetch_func)

    # test subset = all
    bunch = datasets.fetch_20newsgroups_vectorized(subset='all')
    assert_true(sp.isspmatrix_csr(bunch.data))
    assert_equal(bunch.data.shape, (11314 + 7532, 130107))
    assert_equal(bunch.target.shape[0], 11314 + 7532)
    assert_equal(bunch.data.dtype, np.float64)
