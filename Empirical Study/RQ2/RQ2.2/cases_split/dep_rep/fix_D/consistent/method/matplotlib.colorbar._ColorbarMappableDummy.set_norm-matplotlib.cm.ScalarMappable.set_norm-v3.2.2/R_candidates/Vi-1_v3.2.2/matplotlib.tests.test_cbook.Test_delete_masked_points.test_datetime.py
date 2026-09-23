    def test_datetime(self):
        dates = [datetime(2008, 1, 1), datetime(2008, 1, 2),
                 datetime(2008, 1, 3), datetime(2008, 1, 4),
                 datetime(2008, 1, 5), datetime(2008, 1, 6)]
        a_masked = np.ma.array([1, 2, 3, np.nan, np.nan, 6],
                               mask=[False, False, True, True, False, False])
        actual = delete_masked_points(dates, a_masked)
        ind = [0, 1, 5]
        assert_array_equal(actual[0], np.array(dates)[ind])
        assert_array_equal(actual[1], a_masked[ind].compressed())
