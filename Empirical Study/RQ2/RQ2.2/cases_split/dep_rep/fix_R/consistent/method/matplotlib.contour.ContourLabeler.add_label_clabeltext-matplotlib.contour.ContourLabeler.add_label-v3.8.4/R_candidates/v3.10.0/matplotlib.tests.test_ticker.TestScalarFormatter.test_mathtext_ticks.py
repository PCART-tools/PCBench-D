    def test_mathtext_ticks(self):
        mpl.rcParams.update({
            'font.family': 'serif',
            'font.serif': 'cmr10',
            'axes.formatter.use_mathtext': False
        })

        if parse_version(pytest.__version__).major < 8:
            with pytest.warns(UserWarning, match='cmr10 font should ideally'):
                fig, ax = plt.subplots()
                ax.set_xticks([-1, 0, 1])
                fig.canvas.draw()
        else:
            with (pytest.warns(UserWarning, match="Glyph 8722"),
                  pytest.warns(UserWarning, match='cmr10 font should ideally')):
                fig, ax = plt.subplots()
                ax.set_xticks([-1, 0, 1])
                fig.canvas.draw()
