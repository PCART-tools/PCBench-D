    def test_apply_window_1D_els_wrongsize_ValueError(self):
        x = self.sig_rand
        window = mlab.window_hanning(np.ones(x.shape[0]-1))
        with pytest.raises(ValueError):
            _apply_window(x, window)
