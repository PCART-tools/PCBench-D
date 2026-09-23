class TestDetrend:
    def setup(self):
        np.random.seed(0)
        n = 1000
        x = np.linspace(0., 100, n)

        self.sig_zeros = np.zeros(n)

        self.sig_off = self.sig_zeros + 100.
        self.sig_slope = np.linspace(-10., 90., n)
        self.sig_slope_mean = x - x.mean()

        self.sig_base = (
            np.random.standard_normal(n) + np.sin(x*2*np.pi/(n/100)))
        self.sig_base -= self.sig_base.mean()

    def allclose(self, *args):
        assert_allclose(*args, atol=1e-8)

    def test_detrend_none(self):
        assert mlab.detrend_none(0.) == 0.
        assert mlab.detrend_none(0., axis=1) == 0.
        assert mlab.detrend(0., key="none") == 0.
        assert mlab.detrend(0., key=mlab.detrend_none) == 0.
        for sig in [
                5.5, self.sig_off, self.sig_slope, self.sig_base,
                (self.sig_base + self.sig_slope + self.sig_off).tolist(),
                np.vstack([self.sig_base,  # 2D case.
                           self.sig_base + self.sig_off,
                           self.sig_base + self.sig_slope,
                           self.sig_base + self.sig_off + self.sig_slope]),
                np.vstack([self.sig_base,  # 2D transposed case.
                           self.sig_base + self.sig_off,
                           self.sig_base + self.sig_slope,
                           self.sig_base + self.sig_off + self.sig_slope]).T,
        ]:
            if isinstance(sig, np.ndarray):
                assert_array_equal(mlab.detrend_none(sig), sig)
            else:
                assert mlab.detrend_none(sig) == sig

    def test_detrend_mean(self):
        for sig in [0., 5.5]:  # 0D.
            assert mlab.detrend_mean(sig) == 0.
            assert mlab.detrend(sig, key="mean") == 0.
            assert mlab.detrend(sig, key=mlab.detrend_mean) == 0.
        # 1D.
        self.allclose(mlab.detrend_mean(self.sig_zeros), self.sig_zeros)
        self.allclose(mlab.detrend_mean(self.sig_base), self.sig_base)
        self.allclose(mlab.detrend_mean(self.sig_base + self.sig_off),
                      self.sig_base)
        self.allclose(mlab.detrend_mean(self.sig_base + self.sig_slope),
                      self.sig_base + self.sig_slope_mean)
        self.allclose(
            mlab.detrend_mean(self.sig_base + self.sig_slope + self.sig_off),
            self.sig_base + self.sig_slope_mean)

    def test_detrend_mean_1d_base_slope_off_list_andor_axis0(self):
        input = self.sig_base + self.sig_slope + self.sig_off
        target = self.sig_base + self.sig_slope_mean
        self.allclose(mlab.detrend_mean(input, axis=0), target)
        self.allclose(mlab.detrend_mean(input.tolist()), target)
        self.allclose(mlab.detrend_mean(input.tolist(), axis=0), target)

    def test_detrend_mean_2d(self):
        input = np.vstack([self.sig_off,
                           self.sig_base + self.sig_off])
        target = np.vstack([self.sig_zeros,
                            self.sig_base])
        self.allclose(mlab.detrend_mean(input), target)
        self.allclose(mlab.detrend_mean(input, axis=None), target)
        self.allclose(mlab.detrend_mean(input.T, axis=None).T, target)
        self.allclose(mlab.detrend(input), target)
        self.allclose(mlab.detrend(input, axis=None), target)
        self.allclose(
            mlab.detrend(input.T, key="constant", axis=None), target.T)

        input = np.vstack([self.sig_base,
                           self.sig_base + self.sig_off,
                           self.sig_base + self.sig_slope,
                           self.sig_base + self.sig_off + self.sig_slope])
        target = np.vstack([self.sig_base,
                            self.sig_base,
                            self.sig_base + self.sig_slope_mean,
                            self.sig_base + self.sig_slope_mean])
        self.allclose(mlab.detrend_mean(input.T, axis=0), target.T)
        self.allclose(mlab.detrend_mean(input, axis=1), target)
        self.allclose(mlab.detrend_mean(input, axis=-1), target)
        self.allclose(mlab.detrend(input, key="default", axis=1), target)
        self.allclose(mlab.detrend(input.T, key="mean", axis=0), target.T)
        self.allclose(
            mlab.detrend(input.T, key=mlab.detrend_mean, axis=0), target.T)

    def test_detrend_ValueError(self):
        for signal, kwargs in [
                (self.sig_slope[np.newaxis], {"key": "spam"}),
                (self.sig_slope[np.newaxis], {"key": 5}),
                (5.5, {"axis": 0}),
                (self.sig_slope, {"axis": 1}),
                (self.sig_slope[np.newaxis], {"axis": 2}),
        ]:
            with pytest.raises(ValueError):
                mlab.detrend(signal, **kwargs)

    def test_detrend_mean_ValueError(self):
        for signal, kwargs in [
                (5.5, {"axis": 0}),
                (self.sig_slope, {"axis": 1}),
                (self.sig_slope[np.newaxis], {"axis": 2}),
        ]:
            with pytest.raises(ValueError):
                mlab.detrend_mean(signal, **kwargs)

    def test_detrend_linear(self):
        # 0D.
        assert mlab.detrend_linear(0.) == 0.
        assert mlab.detrend_linear(5.5) == 0.
        assert mlab.detrend(5.5, key="linear") == 0.
        assert mlab.detrend(5.5, key=mlab.detrend_linear) == 0.
        for sig in [  # 1D.
                self.sig_off,
                self.sig_slope,
                self.sig_slope + self.sig_off,
        ]:
            self.allclose(mlab.detrend_linear(sig), self.sig_zeros)

    def test_detrend_str_linear_1d(self):
        input = self.sig_slope + self.sig_off
        target = self.sig_zeros
        self.allclose(mlab.detrend(input, key="linear"), target)
        self.allclose(mlab.detrend(input, key=mlab.detrend_linear), target)
        self.allclose(mlab.detrend_linear(input.tolist()), target)

    def test_detrend_linear_2d(self):
        input = np.vstack([self.sig_off,
                           self.sig_slope,
                           self.sig_slope + self.sig_off])
        target = np.vstack([self.sig_zeros,
                            self.sig_zeros,
                            self.sig_zeros])
        self.allclose(
            mlab.detrend(input.T, key="linear", axis=0), target.T)
        self.allclose(
            mlab.detrend(input.T, key=mlab.detrend_linear, axis=0), target.T)
        self.allclose(
            mlab.detrend(input, key="linear", axis=1), target)
        self.allclose(
            mlab.detrend(input, key=mlab.detrend_linear, axis=1), target)

        with pytest.raises(ValueError):
            mlab.detrend_linear(self.sig_slope[np.newaxis])
