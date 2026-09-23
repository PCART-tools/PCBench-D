    def test_boxplot_stats_autorange_false(self):
        x = np.zeros(shape=140)
        x = np.hstack([-25, x, 25])
        bstats_false = cbook.boxplot_stats(x, autorange=False)
        bstats_true = cbook.boxplot_stats(x, autorange=True)

        assert bstats_false[0]['whislo'] == 0
        assert bstats_false[0]['whishi'] == 0
        assert_array_almost_equal(bstats_false[0]['fliers'], [-25, 25])

        assert bstats_true[0]['whislo'] == -25
        assert bstats_true[0]['whishi'] == 25
        assert_array_almost_equal(bstats_true[0]['fliers'], [])
