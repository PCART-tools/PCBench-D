def test_legacy():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)

        # Legacy behavior: truncating arguments to integers
        assert_equal(special.bdtrc(1, 2, 0.3), special.bdtrc(1.8, 2.8, 0.3))
        assert_equal(special.bdtr(1, 2, 0.3), special.bdtr(1.8, 2.8, 0.3))
        assert_equal(special.bdtri(1, 2, 0.3), special.bdtri(1.8, 2.8, 0.3))
        assert_equal(special.expn(1, 0.3), special.expn(1.8, 0.3))
        assert_equal(special.hyp2f0(1, 2, 0.3, 1), special.hyp2f0(1, 2, 0.3, 1.8))
        assert_equal(special.nbdtrc(1, 2, 0.3), special.nbdtrc(1.8, 2.8, 0.3))
        assert_equal(special.nbdtr(1, 2, 0.3), special.nbdtr(1.8, 2.8, 0.3))
        assert_equal(special.nbdtri(1, 2, 0.3), special.nbdtri(1.8, 2.8, 0.3))
        assert_equal(special.pdtrc(1, 0.3), special.pdtrc(1.8, 0.3))
        assert_equal(special.pdtr(1, 0.3), special.pdtr(1.8, 0.3))
        assert_equal(special.pdtri(1, 0.3), special.pdtri(1.8, 0.3))
        assert_equal(special.kn(1, 0.3), special.kn(1.8, 0.3))
        assert_equal(special.yn(1, 0.3), special.yn(1.8, 0.3))
        assert_equal(special.smirnov(1, 0.3), special.smirnov(1.8, 0.3))
        assert_equal(special.smirnovi(1, 0.3), special.smirnovi(1.8, 0.3))
