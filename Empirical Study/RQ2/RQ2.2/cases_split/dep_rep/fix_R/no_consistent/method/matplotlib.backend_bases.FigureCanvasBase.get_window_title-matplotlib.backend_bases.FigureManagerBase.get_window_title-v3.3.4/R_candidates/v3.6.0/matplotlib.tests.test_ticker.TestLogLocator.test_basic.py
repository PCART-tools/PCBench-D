    def test_basic(self):
        loc = mticker.LogLocator(numticks=5)
        with pytest.raises(ValueError):
            loc.tick_values(0, 1000)

        test_value = np.array([1.00000000e-05, 1.00000000e-03, 1.00000000e-01,
                               1.00000000e+01, 1.00000000e+03, 1.00000000e+05,
                               1.00000000e+07, 1.000000000e+09])
        assert_almost_equal(loc.tick_values(0.001, 1.1e5), test_value)

        loc = mticker.LogLocator(base=2)
        test_value = np.array([0.5, 1., 2., 4., 8., 16., 32., 64., 128., 256.])
        assert_almost_equal(loc.tick_values(1, 100), test_value)
