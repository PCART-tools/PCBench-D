class TestLegendFigureFunction:
    # Tests the legend function for figure
    def test_legend_handle_label(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend(lines, ['hello world'])
        Legend.assert_called_with(fig, lines, ['hello world'],
                                  bbox_transform=fig.transFigure)

    def test_legend_no_args(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10), label='hello world')
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend()
        Legend.assert_called_with(fig, lines, ['hello world'],
                                  bbox_transform=fig.transFigure)

    def test_legend_label_arg(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend(['foobar'])
        Legend.assert_called_with(fig, lines, ['foobar'],
                                  bbox_transform=fig.transFigure)

    def test_legend_label_three_args(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend(lines, ['foobar'], 'right')
        Legend.assert_called_with(fig, lines, ['foobar'], 'right',
                                  bbox_transform=fig.transFigure)

    def test_legend_label_three_args_pluskw(self):
        # test that third argument and loc=  called together give
        # Exception
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with pytest.raises(Exception):
            fig.legend(lines, ['foobar'], 'right', loc='left')

    def test_legend_kw_args(self):
        fig, axs = plt.subplots(1, 2)
        lines = axs[0].plot(range(10))
        lines2 = axs[1].plot(np.arange(10) * 2.)
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend(loc='right', labels=('a', 'b'), handles=(lines, lines2))
        Legend.assert_called_with(
            fig, (lines, lines2), ('a', 'b'), loc='right',
            bbox_transform=fig.transFigure)

    def test_warn_args_kwargs(self):
        fig, axs = plt.subplots(1, 2)
        lines = axs[0].plot(range(10))
        lines2 = axs[1].plot(np.arange(10) * 2.)
        with pytest.warns(UserWarning) as record:
            fig.legend((lines, lines2), labels=('a', 'b'))
        assert len(record) == 1
        assert str(record[0].message) == (
            "You have mixed positional and keyword arguments, some input may "
            "be discarded.")
