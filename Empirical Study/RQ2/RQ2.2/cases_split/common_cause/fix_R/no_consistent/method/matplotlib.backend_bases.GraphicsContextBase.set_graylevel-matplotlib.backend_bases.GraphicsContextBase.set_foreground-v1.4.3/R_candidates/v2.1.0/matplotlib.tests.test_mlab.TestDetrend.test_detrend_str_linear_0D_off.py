    def test_detrend_str_linear_0D_off(self):
        input = 5.5
        targ = 0.
        res = mlab.detrend(input, key='linear')
        assert_almost_equal(res, targ)
