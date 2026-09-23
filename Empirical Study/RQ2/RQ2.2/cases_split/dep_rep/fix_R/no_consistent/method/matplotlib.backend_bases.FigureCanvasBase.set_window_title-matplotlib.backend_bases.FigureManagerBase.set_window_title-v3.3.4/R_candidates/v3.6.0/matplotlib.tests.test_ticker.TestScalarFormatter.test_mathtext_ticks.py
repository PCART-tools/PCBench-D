    def test_mathtext_ticks(self):
        mpl.rcParams.update({
            'font.family': 'serif',
            'font.serif': 'cmr10',
            'axes.formatter.use_mathtext': False
        })

        with pytest.warns(UserWarning, match='cmr10 font should ideally'):
            fig, ax = plt.subplots()
            ax.set_xticks([-1, 0, 1])
            fig.canvas.draw()
