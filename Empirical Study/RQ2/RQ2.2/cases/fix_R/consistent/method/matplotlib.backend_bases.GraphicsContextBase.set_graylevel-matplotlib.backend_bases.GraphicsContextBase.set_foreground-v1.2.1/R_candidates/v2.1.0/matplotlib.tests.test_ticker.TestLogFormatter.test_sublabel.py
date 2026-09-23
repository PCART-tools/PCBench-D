    @pytest.mark.style('default')
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
        # were 3, then the label sub would be 3 for 2-3 decades and (2,5)
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
