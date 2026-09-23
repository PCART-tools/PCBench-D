    def test_psd_detrend_linear_func_trend(self):
        if self.NFFT_density is None:
            return
        freqs = self.freqs_density
        ydata = np.arange(self.NFFT_density)
        ydata1 = ydata+5
        ydata2 = ydata+3.3
        ydata = np.vstack([ydata1, ydata2])
        ydata = np.tile(ydata, (20, 1))
        ydatab = ydata.T.flatten()
        ydata = ydata.flatten()
        ycontrol = np.zeros_like(ydata)
        spec_g, fsp_g = mlab.psd(x=ydata,
                                 NFFT=self.NFFT_density,
                                 Fs=self.Fs,
                                 noverlap=0,
                                 sides=self.sides,
                                 detrend=mlab.detrend_linear)
        spec_b, fsp_b = mlab.psd(x=ydatab,
                                 NFFT=self.NFFT_density,
                                 Fs=self.Fs,
                                 noverlap=0,
                                 sides=self.sides,
                                 detrend=mlab.detrend_linear)
        spec_c, fsp_c = mlab.psd(x=ycontrol,
                                 NFFT=self.NFFT_density,
                                 Fs=self.Fs,
                                 noverlap=0,
                                 sides=self.sides)
        assert_array_equal(fsp_g, fsp_c)
        assert_array_equal(fsp_b, fsp_c)
        assert_allclose(spec_g, spec_c, atol=1e-08)
        # these should not be almost equal
        with pytest.raises(AssertionError):
            assert_allclose(spec_b, spec_c, atol=1e-08)
