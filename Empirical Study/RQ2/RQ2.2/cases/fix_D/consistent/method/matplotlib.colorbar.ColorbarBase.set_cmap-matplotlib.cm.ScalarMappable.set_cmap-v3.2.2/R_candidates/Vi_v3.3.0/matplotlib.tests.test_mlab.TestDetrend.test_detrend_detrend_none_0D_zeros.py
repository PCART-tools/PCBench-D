    def test_detrend_detrend_none_0D_zeros(self):
        input = 0.
        targ = input
        mlab.detrend(input, key=mlab.detrend_none)
        assert input == targ
