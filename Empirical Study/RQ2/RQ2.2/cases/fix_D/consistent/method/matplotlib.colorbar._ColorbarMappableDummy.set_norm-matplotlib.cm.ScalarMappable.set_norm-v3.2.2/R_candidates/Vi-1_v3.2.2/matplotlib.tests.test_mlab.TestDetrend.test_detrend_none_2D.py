    def test_detrend_none_2D(self):
        arri = [self.sig_base,
                self.sig_base + self.sig_off,
                self.sig_base + self.sig_slope,
                self.sig_base + self.sig_off + self.sig_slope]
        input = np.vstack(arri)
        targ = input
        res = mlab.detrend_none(input)
        assert_array_equal(res, targ)
