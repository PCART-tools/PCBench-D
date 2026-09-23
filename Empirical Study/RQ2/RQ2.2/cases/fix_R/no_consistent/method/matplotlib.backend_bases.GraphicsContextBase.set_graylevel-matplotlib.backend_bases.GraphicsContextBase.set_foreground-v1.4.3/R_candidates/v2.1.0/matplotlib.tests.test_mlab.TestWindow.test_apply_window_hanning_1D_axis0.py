    def test_apply_window_hanning_1D_axis0(self):
        x = self.sig_rand
        window = mlab.window_hanning
        y = mlab.apply_window(x, window, axis=0, return_window=False)
        yt = window(x)
        assert yt.shape == y.shape
        assert x.shape == y.shape
        assert_allclose(yt, y, atol=1e-06)
