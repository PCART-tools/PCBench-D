    def test_apply_window_hanning_2D__els1_axis1(self):
        x = np.random.standard_normal([10, 1000]) + 100.
        window = mlab.window_hanning(np.ones(x.shape[1]))
        window1 = mlab.window_hanning
        y = _apply_window(x, window, axis=1, return_window=False)
        yt = np.zeros_like(x)
        for i in range(x.shape[0]):
            yt[i, :] = window1(x[i, :])
        assert yt.shape == y.shape
        assert x.shape == y.shape
        assert_allclose(yt, y, atol=1e-06)
