    def test_line_extent_data_coords(self):
        # a simple line in data coordinates
        ax = plt.axes()
        ax.plot([0.1, 1.2, 0.8], [0.9, 0.5, 0.8], transform=ax.transData)
        assert_array_equal(ax.dataLim.get_points(),
                           np.array([[0.1,  0.5], [1.2,  0.9]]))
