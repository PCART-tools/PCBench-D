    def test_window_hanning_ones(self):
        targ = np.hanning(len(self.sig_ones))
        res = mlab.window_hanning(self.sig_ones)

        assert_allclose(targ, res, atol=1e-06)
