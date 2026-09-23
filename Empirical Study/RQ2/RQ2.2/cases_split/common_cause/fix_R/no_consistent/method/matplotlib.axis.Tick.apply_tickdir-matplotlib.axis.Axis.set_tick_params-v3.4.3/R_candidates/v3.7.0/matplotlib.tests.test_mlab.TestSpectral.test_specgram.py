    @pytest.mark.parametrize(
        'kwargs',
        [{}, {'mode': 'default'}, {'mode': 'psd'}, {'mode': 'magnitude'},
         {'mode': 'complex'}, {'mode': 'angle'}, {'mode': 'phase'}])
    def test_specgram(self, kwargs):
        freqs = self.freqs_specgram
        spec, fsp, t = mlab.specgram(x=self.y,
                                     NFFT=self.NFFT_specgram,
                                     Fs=self.Fs,
                                     noverlap=self.nover_specgram,
                                     pad_to=self.pad_to_specgram,
                                     sides=self.sides,
                                     **kwargs)
        if kwargs.get('mode') == 'complex':
            spec = np.abs(spec)
        specm = np.mean(spec, axis=1)

        assert_allclose(fsp, freqs, atol=1e-06)
        assert_allclose(t, self.t_specgram, atol=1e-06)

        assert spec.shape[0] == freqs.shape[0]
        assert spec.shape[1] == self.t_specgram.shape[0]

        if kwargs.get('mode') not in ['complex', 'angle', 'phase']:
            # using a single freq, so all time slices should be about the same
            if np.abs(spec.max()) != 0:
                assert_allclose(
                    np.diff(spec, axis=1).max() / np.abs(spec.max()), 0,
                    atol=1e-02)
        if kwargs.get('mode') not in ['angle', 'phase']:
            self.check_freqs(specm, freqs, fsp, self.fstims)
