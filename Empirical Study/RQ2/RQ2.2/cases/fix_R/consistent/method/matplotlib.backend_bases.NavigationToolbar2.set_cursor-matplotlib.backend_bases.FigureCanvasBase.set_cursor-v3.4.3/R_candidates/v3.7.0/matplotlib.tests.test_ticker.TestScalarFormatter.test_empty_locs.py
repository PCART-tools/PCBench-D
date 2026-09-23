    def test_empty_locs(self):
        sf = mticker.ScalarFormatter()
        sf.set_locs([])
        assert sf(0.5) == ''
