    def test_psd_window_hanning(self):
        if self.NFFT_density is None:
            return
        freqs = self.freqs_density
        ydata = np.arange(self.NFFT_density)
        ydata1 = ydata+5
        ydata2 = ydata+3.3
        ycontrol1, windowVals = mlab.apply_window(ydata1,
                                                  mlab.window_hanning,
                                                  return_window=True)
        ycontrol2 = mlab.window_hanning(ydata2)
        ydata = np.vstack([ydata1, ydata2])
        ycontrol = np.vstack([ycontrol1, ycontrol2])
        ydata = np.tile(ydata, (20, 1))
        ycontrol = np.tile(ycontrol, (20, 1))
        ydatab = ydata.T.flatten()
        ydataf = ydata.flatten()
        ycontrol = ycontrol.flatten()
        spec_g, fsp_g = mlab.psd(x=ydataf,
                                 NFFT=self.NFFT_density,
                                 Fs=self.Fs,
                                 noverlap=0,
                                 sides=self.sides,
                                 window=mlab.window_hanning)
        spec_b, fsp_b = mlab.psd(x=ydatab,
                                 NFFT=self.NFFT_density,
                                 Fs=self.Fs,
                                 noverlap=0,
                                 sides=self.sides,
                                 window=mlab.window_hanning)
        spec_c, fsp_c = mlab.psd(x=ycontrol,
                                 NFFT=self.NFFT_density,
                                 Fs=self.Fs,
                                 noverlap=0,
                                 sides=self.sides,
                                 window=mlab.window_none)
        spec_c *= len(ycontrol1)/(np.abs(windowVals)**2).sum()
        assert_array_equal(fsp_g, fsp_c)
        assert_array_equal(fsp_b, fsp_c)
        assert_allclose(spec_g, spec_c, atol=1e-08)
        # these should not be almost equal
        with pytest.raises(AssertionError):
            assert_allclose(spec_b, spec_c, atol=1e-08)
