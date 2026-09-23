    def test_detrend_none_1D_base_slope_off_list(self):
        input = self.sig_base + self.sig_slope + self.sig_off
        targ = input.tolist()
        res = mlab.detrend_none(input.tolist())
        assert res == targ
