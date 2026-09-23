    def test_legend_label_three_args_pluskw(self):
        # test that third argument and loc=  called together give
        # Exception
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with pytest.raises(Exception):
            fig.legend(lines, ['foobar'], 'right', loc='left')
