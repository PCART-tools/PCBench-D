    @pytest.mark.parametrize(
        "kind", ["complex", "magnitude", "angle", "phase"])
    def test_spectrum(self, kind):
        freqs = self.freqs_spectrum
        spec, fsp = getattr(mlab, f"{kind}_spectrum")(
            x=self.y,
            Fs=self.Fs, sides=self.sides, pad_to=self.pad_to_spectrum)
        assert_allclose(fsp, freqs, atol=1e-06)
        assert spec.shape == freqs.shape
        if kind == "magnitude":
            self.check_maxfreq(spec, fsp, self.fstims)
            self.check_freqs(spec, freqs, fsp, self.fstims)
