    def test_detrend_none_0D_off(self):
        input = 5.5
        targ = input
        mlab.detrend_none(input)
        assert input == targ
