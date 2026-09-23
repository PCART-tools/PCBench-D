    def test_apply_window_hanning_2D_els3_axis1(self):
        x = np.random.standard_normal([10, 1000]) + 100.
        window = mlab.window_hanning
        window1 = mlab.window_hanning(np.ones(x.shape[1]))
        y = mlab.apply_window(x, window, axis=1, return_window=False)
        yt = mlab.apply_window(x, window1, axis=1, return_window=False)
        assert yt.shape == y.shape
        assert x.shape == y.shape
        assert_allclose(yt, y, atol=1e-06)
