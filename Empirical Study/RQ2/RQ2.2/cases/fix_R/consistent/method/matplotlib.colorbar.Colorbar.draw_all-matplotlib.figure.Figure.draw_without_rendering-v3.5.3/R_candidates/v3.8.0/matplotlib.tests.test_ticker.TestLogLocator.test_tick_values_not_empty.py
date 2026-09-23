    def test_tick_values_not_empty(self):
        mpl.rcParams['_internal.classic_mode'] = False
        ll = mticker.LogLocator(subs=(1, 2, 5))
        test_value = np.array([1.e-01, 2.e-01, 5.e-01, 1.e+00, 2.e+00, 5.e+00,
                               1.e+01, 2.e+01, 5.e+01, 1.e+02, 2.e+02, 5.e+02,
                               1.e+03, 2.e+03, 5.e+03, 1.e+04, 2.e+04, 5.e+04,
                               1.e+05, 2.e+05, 5.e+05, 1.e+06, 2.e+06, 5.e+06,
                               1.e+07, 2.e+07, 5.e+07, 1.e+08, 2.e+08, 5.e+08,
                               1.e+09, 2.e+09, 5.e+09])
        assert_almost_equal(ll.tick_values(1, 1e8), test_value)
