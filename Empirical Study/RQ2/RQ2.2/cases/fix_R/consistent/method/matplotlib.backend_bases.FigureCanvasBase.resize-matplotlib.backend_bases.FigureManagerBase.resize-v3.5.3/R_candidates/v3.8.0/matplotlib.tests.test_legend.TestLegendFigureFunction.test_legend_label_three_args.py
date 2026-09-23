    def test_legend_label_three_args(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with pytest.raises(TypeError, match="0-2"):
            fig.legend(lines, ['foobar'], 'right')
        with pytest.raises(TypeError, match="0-2"):
            fig.legend(lines, ['foobar'], 'right', loc='left')
