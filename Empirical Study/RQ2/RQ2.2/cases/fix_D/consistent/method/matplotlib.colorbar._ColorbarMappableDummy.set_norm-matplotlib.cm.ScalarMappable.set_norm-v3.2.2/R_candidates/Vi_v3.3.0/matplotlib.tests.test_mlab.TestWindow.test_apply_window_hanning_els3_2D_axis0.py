    def test_apply_window_hanning_els3_2D_axis0(self):
        x = np.random.standard_normal([1000, 10]) + 100.
        window = mlab.window_hanning
        window1 = mlab.window_hanning(np.ones(x.shape[0]))
        y, window2 = _apply_window(x, window, axis=0, return_window=True)
        yt = _apply_window(x, window1, axis=0, return_window=False)
        assert yt.shape == y.shape
        assert x.shape == y.shape
        assert_allclose(yt, y, atol=1e-06)
        assert_array_equal(window1, window2)
