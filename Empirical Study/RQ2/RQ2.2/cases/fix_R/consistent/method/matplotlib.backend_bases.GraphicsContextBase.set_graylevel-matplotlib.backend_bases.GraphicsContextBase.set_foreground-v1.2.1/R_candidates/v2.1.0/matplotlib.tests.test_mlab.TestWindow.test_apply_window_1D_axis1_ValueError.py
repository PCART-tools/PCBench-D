    def test_apply_window_1D_axis1_ValueError(self):
        x = self.sig_rand
        window = mlab.window_hanning
        with pytest.raises(ValueError):
            mlab.apply_window(x, window, axis=1, return_window=False)
