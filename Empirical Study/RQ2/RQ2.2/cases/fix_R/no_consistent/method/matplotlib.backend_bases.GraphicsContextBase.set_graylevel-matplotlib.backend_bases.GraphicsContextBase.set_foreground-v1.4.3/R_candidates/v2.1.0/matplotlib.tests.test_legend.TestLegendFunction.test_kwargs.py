    def test_kwargs(self):
        fig, ax = plt.subplots(1, 1)
        th = np.linspace(0, 2*np.pi, 1024)
        lns, = ax.plot(th, np.sin(th), label='sin', lw=5)
        lnc, = ax.plot(th, np.cos(th), label='cos', lw=5)
        with mock.patch('matplotlib.legend.Legend') as Legend:
            ax.legend(handles=(lnc, lns), labels=('a', 'b'))
        Legend.assert_called_with(ax, (lnc, lns), ('a', 'b'))
