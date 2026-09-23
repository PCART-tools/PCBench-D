def test_ncx2_tails_pdf():
    # ncx2.pdf does not return nans in extreme tails(example from gh-1577)
    # NB: this is to check that nan_to_num is not needed in ncx2.pdf
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        assert_equal(stats.ncx2.pdf(1, np.arange(340, 350), 2), 0)
        logval = stats.ncx2.logpdf(1, np.arange(340, 350), 2)
        assert_(np.isneginf(logval).all())
