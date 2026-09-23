    def test_detrend_none_1D_base(self):
        input = self.sig_base
        targ = input
        res = mlab.detrend_none(input)
        assert_array_equal(res, targ)
