    def test_apply_window_hanning_1D(self):
        x = self.sig_rand
        window = mlab.window_hanning
        window1 = mlab.window_hanning(np.ones(x.shape[0]))
        y, window2 = mlab.apply_window(x, window, return_window=True)
        yt = window(x)
        assert yt.shape == y.shape
        assert x.shape == y.shape
        assert_allclose(yt, y, atol=1e-06)
        assert_array_equal(window1, window2)
