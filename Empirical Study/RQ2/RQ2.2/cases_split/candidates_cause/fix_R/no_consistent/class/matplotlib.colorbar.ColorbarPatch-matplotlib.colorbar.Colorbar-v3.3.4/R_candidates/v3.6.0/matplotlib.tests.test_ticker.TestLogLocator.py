class TestLogLocator:
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

    def test_switch_to_autolocator(self):
        loc = mticker.LogLocator(subs="all")
        assert_array_equal(loc.tick_values(0.45, 0.55),
                           [0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56])
        # check that we *skip* 1.0, and 10, because this is a minor locator
        loc = mticker.LogLocator(subs=np.arange(2, 10))
        assert 1.0 not in loc.tick_values(0.9, 20.)
        assert 10.0 not in loc.tick_values(0.9, 20.)

    def test_set_params(self):
        """
        Create log locator with default value, base=10.0, subs=[1.0],
        numdecs=4, numticks=15 and change it to something else.
        See if change was successful. Should not raise exception.
        """
        loc = mticker.LogLocator()
        loc.set_params(numticks=7, numdecs=8, subs=[2.0], base=4)
        assert loc.numticks == 7
        assert loc.numdecs == 8
        assert loc._base == 4
        assert list(loc._subs) == [2.0]
