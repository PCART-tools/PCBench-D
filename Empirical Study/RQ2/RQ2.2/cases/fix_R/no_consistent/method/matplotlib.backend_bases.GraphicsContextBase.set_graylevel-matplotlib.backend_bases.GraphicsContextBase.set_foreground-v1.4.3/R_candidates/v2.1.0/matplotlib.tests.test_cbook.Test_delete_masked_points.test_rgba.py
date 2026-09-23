    def test_rgba(self):
        actual = dmp(self.arr3, self.arr_rgba)
        ind = [0, 1, 5]
        expected = (self.arr3.take(ind).compressed(),
                    self.arr_rgba.take(ind, axis=0))
        assert_array_equal(actual[0], expected[0])
        assert_array_equal(actual[1], expected[1])
