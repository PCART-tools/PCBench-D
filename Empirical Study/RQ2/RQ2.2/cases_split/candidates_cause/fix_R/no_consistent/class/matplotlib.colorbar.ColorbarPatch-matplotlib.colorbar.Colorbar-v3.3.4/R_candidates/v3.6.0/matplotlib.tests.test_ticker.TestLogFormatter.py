class TestLogFormatter:
    pprint_data = [
        (3.141592654e-05, 0.001, '3.142e-5'),
        (0.0003141592654, 0.001, '3.142e-4'),
        (0.003141592654, 0.001, '3.142e-3'),
        (0.03141592654, 0.001, '3.142e-2'),
        (0.3141592654, 0.001, '3.142e-1'),
        (3.141592654, 0.001, '3.142'),
        (31.41592654, 0.001, '3.142e1'),
        (314.1592654, 0.001, '3.142e2'),
        (3141.592654, 0.001, '3.142e3'),
        (31415.92654, 0.001, '3.142e4'),
        (314159.2654, 0.001, '3.142e5'),
        (1e-05, 0.001, '1e-5'),
        (0.0001, 0.001, '1e-4'),
        (0.001, 0.001, '1e-3'),
        (0.01, 0.001, '1e-2'),
        (0.1, 0.001, '1e-1'),
        (1, 0.001, '1'),
        (10, 0.001, '10'),
        (100, 0.001, '100'),
        (1000, 0.001, '1000'),
        (10000, 0.001, '1e4'),
        (100000, 0.001, '1e5'),
        (3.141592654e-05, 0.015, '0'),
        (0.0003141592654, 0.015, '0'),
        (0.003141592654, 0.015, '0.003'),
        (0.03141592654, 0.015, '0.031'),
        (0.3141592654, 0.015, '0.314'),
        (3.141592654, 0.015, '3.142'),
        (31.41592654, 0.015, '31.416'),
        (314.1592654, 0.015, '314.159'),
        (3141.592654, 0.015, '3141.593'),
        (31415.92654, 0.015, '31415.927'),
        (314159.2654, 0.015, '314159.265'),
        (1e-05, 0.015, '0'),
        (0.0001, 0.015, '0'),
        (0.001, 0.015, '0.001'),
        (0.01, 0.015, '0.01'),
        (0.1, 0.015, '0.1'),
        (1, 0.015, '1'),
        (10, 0.015, '10'),
        (100, 0.015, '100'),
        (1000, 0.015, '1000'),
        (10000, 0.015, '10000'),
        (100000, 0.015, '100000'),
        (3.141592654e-05, 0.5, '0'),
        (0.0003141592654, 0.5, '0'),
        (0.003141592654, 0.5, '0.003'),
        (0.03141592654, 0.5, '0.031'),
        (0.3141592654, 0.5, '0.314'),
        (3.141592654, 0.5, '3.142'),
        (31.41592654, 0.5, '31.416'),
        (314.1592654, 0.5, '314.159'),
        (3141.592654, 0.5, '3141.593'),
        (31415.92654, 0.5, '31415.927'),
        (314159.2654, 0.5, '314159.265'),
        (1e-05, 0.5, '0'),
        (0.0001, 0.5, '0'),
        (0.001, 0.5, '0.001'),
        (0.01, 0.5, '0.01'),
        (0.1, 0.5, '0.1'),
        (1, 0.5, '1'),
        (10, 0.5, '10'),
        (100, 0.5, '100'),
        (1000, 0.5, '1000'),
        (10000, 0.5, '10000'),
        (100000, 0.5, '100000'),
        (3.141592654e-05, 5, '0'),
        (0.0003141592654, 5, '0'),
        (0.003141592654, 5, '0'),
        (0.03141592654, 5, '0.03'),
        (0.3141592654, 5, '0.31'),
        (3.141592654, 5, '3.14'),
        (31.41592654, 5, '31.42'),
        (314.1592654, 5, '314.16'),
        (3141.592654, 5, '3141.59'),
        (31415.92654, 5, '31415.93'),
        (314159.2654, 5, '314159.27'),
        (1e-05, 5, '0'),
        (0.0001, 5, '0'),
        (0.001, 5, '0'),
        (0.01, 5, '0.01'),
        (0.1, 5, '0.1'),
        (1, 5, '1'),
        (10, 5, '10'),
        (100, 5, '100'),
        (1000, 5, '1000'),
        (10000, 5, '10000'),
        (100000, 5, '100000'),
        (3.141592654e-05, 100, '0'),
        (0.0003141592654, 100, '0'),
        (0.003141592654, 100, '0'),
        (0.03141592654, 100, '0'),
        (0.3141592654, 100, '0.3'),
        (3.141592654, 100, '3.1'),
        (31.41592654, 100, '31.4'),
        (314.1592654, 100, '314.2'),
        (3141.592654, 100, '3141.6'),
        (31415.92654, 100, '31415.9'),
        (314159.2654, 100, '314159.3'),
        (1e-05, 100, '0'),
        (0.0001, 100, '0'),
        (0.001, 100, '0'),
        (0.01, 100, '0'),
        (0.1, 100, '0.1'),
        (1, 100, '1'),
        (10, 100, '10'),
        (100, 100, '100'),
        (1000, 100, '1000'),
        (10000, 100, '10000'),
        (100000, 100, '100000'),
        (3.141592654e-05, 1000000.0, '3.1e-5'),
        (0.0003141592654, 1000000.0, '3.1e-4'),
        (0.003141592654, 1000000.0, '3.1e-3'),
        (0.03141592654, 1000000.0, '3.1e-2'),
        (0.3141592654, 1000000.0, '3.1e-1'),
        (3.141592654, 1000000.0, '3.1'),
        (31.41592654, 1000000.0, '3.1e1'),
        (314.1592654, 1000000.0, '3.1e2'),
        (3141.592654, 1000000.0, '3.1e3'),
        (31415.92654, 1000000.0, '3.1e4'),
        (314159.2654, 1000000.0, '3.1e5'),
        (1e-05, 1000000.0, '1e-5'),
        (0.0001, 1000000.0, '1e-4'),
        (0.001, 1000000.0, '1e-3'),
        (0.01, 1000000.0, '1e-2'),
        (0.1, 1000000.0, '1e-1'),
        (1, 1000000.0, '1'),
        (10, 1000000.0, '10'),
        (100, 1000000.0, '100'),
        (1000, 1000000.0, '1000'),
        (10000, 1000000.0, '1e4'),
        (100000, 1000000.0, '1e5'),
    ]

    @pytest.mark.parametrize('value, domain, expected', pprint_data)
    def test_pprint(self, value, domain, expected):
        fmt = mticker.LogFormatter()
        label = fmt._pprint_val(value, domain)
        assert label == expected

    def _sub_labels(self, axis, subs=()):
        """Test whether locator marks subs to be labeled."""
        fmt = axis.get_minor_formatter()
        minor_tlocs = axis.get_minorticklocs()
        fmt.set_locs(minor_tlocs)
        coefs = minor_tlocs / 10**(np.floor(np.log10(minor_tlocs)))
        label_expected = [round(c) in subs for c in coefs]
        label_test = [fmt(x) != '' for x in minor_tlocs]
        assert label_test == label_expected

    @mpl.style.context('default')
    def test_sublabel(self):
        # test label locator
        fig, ax = plt.subplots()
        ax.set_xscale('log')
        ax.xaxis.set_major_locator(mticker.LogLocator(base=10, subs=[]))
        ax.xaxis.set_minor_locator(mticker.LogLocator(base=10,
                                                      subs=np.arange(2, 10)))
        ax.xaxis.set_major_formatter(mticker.LogFormatter(labelOnlyBase=True))
        ax.xaxis.set_minor_formatter(mticker.LogFormatter(labelOnlyBase=False))
        # axis range above 3 decades, only bases are labeled
        ax.set_xlim(1, 1e4)
        fmt = ax.xaxis.get_major_formatter()
        fmt.set_locs(ax.xaxis.get_majorticklocs())
        show_major_labels = [fmt(x) != ''
                             for x in ax.xaxis.get_majorticklocs()]
        assert np.all(show_major_labels)
        self._sub_labels(ax.xaxis, subs=[])

        # For the next two, if the numdec threshold in LogFormatter.set_locs
        # were 3, then the label sub would be 3 for 2-3 decades and (2, 5)
        # for 1-2 decades.  With a threshold of 1, subs are not labeled.
        # axis range at 2 to 3 decades
        ax.set_xlim(1, 800)
        self._sub_labels(ax.xaxis, subs=[])

        # axis range at 1 to 2 decades
        ax.set_xlim(1, 80)
        self._sub_labels(ax.xaxis, subs=[])

        # axis range at 0.4 to 1 decades, label subs 2, 3, 4, 6
        ax.set_xlim(1, 8)
        self._sub_labels(ax.xaxis, subs=[2, 3, 4, 6])

        # axis range at 0 to 0.4 decades, label all
        ax.set_xlim(0.5, 0.9)
        self._sub_labels(ax.xaxis, subs=np.arange(2, 10, dtype=int))

    @pytest.mark.parametrize('val', [1, 10, 100, 1000])
    def test_LogFormatter_call(self, val):
        # test _num_to_string method used in __call__
        temp_lf = mticker.LogFormatter()
        temp_lf.axis = FakeAxis()
        assert temp_lf(val) == str(val)

    @pytest.mark.parametrize('val', [1e-323, 2e-323, 10e-323, 11e-323])
    def test_LogFormatter_call_tiny(self, val):
        # test coeff computation in __call__
        temp_lf = mticker.LogFormatter()
        temp_lf.axis = FakeAxis()
        temp_lf(val)
