    def test_apply_window_0D_ValueError(self):
        x = np.array(0)
        window = mlab.window_hanning
        with pytest.raises(ValueError):
            mlab.apply_window(x, window, axis=1, return_window=False)
