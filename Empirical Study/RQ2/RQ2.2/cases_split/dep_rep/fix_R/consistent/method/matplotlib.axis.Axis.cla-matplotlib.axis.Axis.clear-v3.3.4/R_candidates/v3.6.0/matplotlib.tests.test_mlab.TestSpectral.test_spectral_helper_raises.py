    def test_spectral_helper_raises(self):
        # We don't use parametrize here to handle ``y = self.y``.
        for kwargs in [  # Various error conditions:
            {"y": self.y+1, "mode": "complex"},  # Modes requiring ``x is y``.
            {"y": self.y+1, "mode": "magnitude"},
            {"y": self.y+1, "mode": "angle"},
            {"y": self.y+1, "mode": "phase"},
            {"mode": "spam"},  # Bad mode.
            {"y": self.y, "sides": "eggs"},  # Bad sides.
            {"y": self.y, "NFFT": 10, "noverlap": 20},  # noverlap > NFFT.
            {"NFFT": 10, "noverlap": 10},  # noverlap == NFFT.
            {"y": self.y, "NFFT": 10,
             "window": np.ones(9)},  # len(win) != NFFT.
        ]:
            with pytest.raises(ValueError):
                mlab._spectral_helper(x=self.y, **kwargs)
