    def test_window_hanning_rand(self):
        targ = np.hanning(len(self.sig_rand)) * self.sig_rand
        res = mlab.window_hanning(self.sig_rand)

        assert_allclose(targ, res, atol=1e-06)
