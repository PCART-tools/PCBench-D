    def test_apply_window_hanning_els_1D_axis0(self):
        x = self.sig_rand
        window = mlab.window_hanning(np.ones(x.shape[0]))
        window1 = mlab.window_hanning
        y = _apply_window(x, window, axis=0, return_window=False)
        yt = window1(x)
        assert yt.shape == y.shape
        assert x.shape == y.shape
        assert_allclose(yt, y, atol=1e-06)
