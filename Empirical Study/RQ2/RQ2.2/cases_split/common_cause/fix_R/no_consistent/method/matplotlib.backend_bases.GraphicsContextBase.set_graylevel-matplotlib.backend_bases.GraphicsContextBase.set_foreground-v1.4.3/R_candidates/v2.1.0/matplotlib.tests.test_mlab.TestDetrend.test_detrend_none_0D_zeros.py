    def test_detrend_none_0D_zeros(self):
        input = 0.
        targ = input
        res = mlab.detrend_none(input)
        assert input == targ
