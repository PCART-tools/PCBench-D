    def test_apply_window_3D_ValueError(self):
        x = self.sig_rand[np.newaxis][np.newaxis]
        window = mlab.window_hanning
        with pytest.raises(ValueError):
            mlab.apply_window(x, window, axis=1, return_window=False)
