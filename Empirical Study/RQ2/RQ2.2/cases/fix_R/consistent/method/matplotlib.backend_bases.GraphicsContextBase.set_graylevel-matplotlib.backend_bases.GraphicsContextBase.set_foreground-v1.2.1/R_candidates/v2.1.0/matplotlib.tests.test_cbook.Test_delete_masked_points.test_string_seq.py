    def test_string_seq(self):
        actual = dmp(self.arr_s, self.arr1)
        ind = [0, 1, 2, 5]
        expected = (self.arr_s2.take(ind), self.arr2.take(ind))
        assert_array_equal(actual[0], expected[0])
        assert_array_equal(actual[1], expected[1])
