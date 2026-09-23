    def test_cmr10_substitutions(self, caplog):
        mpl.rcParams.update({
            'font.family': 'cmr10',
            'mathtext.fontset': 'cm',
            'axes.formatter.use_mathtext': True,
        })

        # Test that it does not log a warning about missing glyphs.
        with caplog.at_level(logging.WARNING, logger='matplotlib.mathtext'):
            fig, ax = plt.subplots()
            ax.plot([-0.03, 0.05], [40, 0.05])
            ax.set_yscale('log')
            yticks = [0.02, 0.3, 4, 50]
            formatter = mticker.LogFormatterSciNotation()
            ax.set_yticks(yticks, map(formatter, yticks))
            fig.canvas.draw()
            assert not caplog.text
