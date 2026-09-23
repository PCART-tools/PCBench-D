    def test_StrCategoryLocator(self):
        locs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ticks = cat.StrCategoryLocator(locs)
        np.testing.assert_array_equal(ticks.tick_values(None, None), locs)
