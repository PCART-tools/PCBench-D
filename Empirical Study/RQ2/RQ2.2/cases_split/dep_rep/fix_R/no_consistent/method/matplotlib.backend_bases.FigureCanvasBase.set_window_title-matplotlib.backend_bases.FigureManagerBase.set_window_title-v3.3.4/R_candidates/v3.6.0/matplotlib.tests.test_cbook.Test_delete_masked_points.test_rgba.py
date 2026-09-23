    def test_rgba(self):
        a_masked = np.ma.array([1, 2, 3, np.nan, np.nan, 6],
                               mask=[False, False, True, True, False, False])
        a_rgba = mcolors.to_rgba_array(['r', 'g', 'b', 'c', 'm', 'y'])
        actual = delete_masked_points(a_masked, a_rgba)
        ind = [0, 1, 5]
        assert_array_equal(actual[0], a_masked[ind].compressed())
        assert_array_equal(actual[1], a_rgba[ind])
