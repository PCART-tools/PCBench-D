    def test_apply_window_hanning_2D_axis0(self):
        x = np.random.standard_normal([1000, 10]) + 100.
        window = mlab.window_hanning
        y = _apply_window(x, window, axis=0, return_window=False)
        yt = np.zeros_like(x)
        for i in range(x.shape[1]):
            yt[:, i] = window(x[:, i])
        assert yt.shape == y.shape
        assert x.shape == y.shape
        assert_allclose(yt, y, atol=1e-06)
