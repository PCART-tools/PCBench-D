    @pytest.mark.style('default')
    def test_scatter_unfillable(self):
        coll = plt.scatter([0, 1, 2], [1, 3, 2], c=['0.1', '0.3', '0.5'],
                           marker='x',
                           linewidths=[1.1, 1.2, 1.3])
        assert_array_equal(coll.get_facecolors(), coll.get_edgecolors())
        assert_array_equal(coll.get_edgecolors(), [[0.1, 0.1, 0.1, 1],
                                                   [0.3, 0.3, 0.3, 1],
                                                   [0.5, 0.5, 0.5, 1]])
        assert_array_equal(coll.get_linewidths(), [1.1, 1.2, 1.3])
