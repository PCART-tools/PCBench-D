    def test_legend_kwargs_handles_labels(self):
        fig, ax = plt.subplots()
        th = np.linspace(0, 2*np.pi, 1024)
        lns, = ax.plot(th, np.sin(th), label='sin')
        lnc, = ax.plot(th, np.cos(th), label='cos')
        with mock.patch('matplotlib.legend.Legend') as Legend:
            # labels of lns, lnc are overwritten with explicit ('a', 'b')
            ax.legend(labels=('a', 'b'), handles=(lnc, lns))
        Legend.assert_called_with(ax, (lnc, lns), ('a', 'b'))
