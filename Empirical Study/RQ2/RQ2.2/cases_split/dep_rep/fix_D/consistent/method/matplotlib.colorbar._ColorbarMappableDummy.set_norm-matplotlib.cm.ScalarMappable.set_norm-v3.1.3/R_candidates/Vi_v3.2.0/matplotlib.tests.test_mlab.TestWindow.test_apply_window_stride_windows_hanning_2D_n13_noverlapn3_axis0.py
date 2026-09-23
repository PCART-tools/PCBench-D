    def test_apply_window_stride_windows_hanning_2D_n13_noverlapn3_axis0(self):
        x = self.sig_rand
        window = mlab.window_hanning
        yi = mlab.stride_windows(x, n=13, noverlap=2, axis=0)
        y = _apply_window(yi, window, axis=0, return_window=False)
        yt = self.check_window_apply_repeat(x, window, 13, 2)
        assert yt.shape == y.shape
        assert x.shape != y.shape
        assert_allclose(yt, y, atol=1e-06)
