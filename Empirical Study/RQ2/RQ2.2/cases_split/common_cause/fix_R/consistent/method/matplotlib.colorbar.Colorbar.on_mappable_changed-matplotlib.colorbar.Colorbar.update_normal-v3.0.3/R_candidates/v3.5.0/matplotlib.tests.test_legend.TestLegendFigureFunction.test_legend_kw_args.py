    def test_legend_kw_args(self):
        fig, axs = plt.subplots(1, 2)
        lines = axs[0].plot(range(10))
        lines2 = axs[1].plot(np.arange(10) * 2.)
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend(loc='right', labels=('a', 'b'), handles=(lines, lines2))
        Legend.assert_called_with(
            fig, (lines, lines2), ('a', 'b'), loc='right',
            bbox_transform=fig.transFigure)
