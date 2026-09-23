    def test_detrend_str_none_0D_zeros(self):
        input = 0.
        targ = input
        mlab.detrend(input, key='none')
        assert input == targ
