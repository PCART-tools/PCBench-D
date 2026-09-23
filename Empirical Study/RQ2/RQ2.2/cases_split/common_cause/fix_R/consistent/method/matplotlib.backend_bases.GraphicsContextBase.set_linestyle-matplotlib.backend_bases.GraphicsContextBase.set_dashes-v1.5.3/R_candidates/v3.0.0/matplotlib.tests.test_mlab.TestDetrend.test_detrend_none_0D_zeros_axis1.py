    def test_detrend_none_0D_zeros_axis1(self):
        input = 0.
        targ = input
        res = mlab.detrend_none(input, axis=1)
        assert input == targ
