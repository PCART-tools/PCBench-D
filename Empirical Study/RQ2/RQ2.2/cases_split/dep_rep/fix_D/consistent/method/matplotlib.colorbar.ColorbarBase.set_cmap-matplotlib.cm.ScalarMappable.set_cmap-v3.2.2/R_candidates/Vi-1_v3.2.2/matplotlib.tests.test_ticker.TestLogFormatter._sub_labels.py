    def _sub_labels(self, axis, subs=()):
        "Test whether locator marks subs to be labeled"
        fmt = axis.get_minor_formatter()
        minor_tlocs = axis.get_minorticklocs()
        fmt.set_locs(minor_tlocs)
        coefs = minor_tlocs / 10**(np.floor(np.log10(minor_tlocs)))
        label_expected = [round(c) in subs for c in coefs]
        label_test = [fmt(x) != '' for x in minor_tlocs]
        assert label_test == label_expected
