    def test_datetime(self):
        actual = dmp(self.arr_dt, self.arr3)
        ind = [0, 1, 5]
        expected = (self.arr_dt2[ind], self.arr3[ind].compressed())
        assert_array_equal(actual[0], expected[0])
        assert_array_equal(actual[1], expected[1])
