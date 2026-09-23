    def test_window_none_rand(self):
        res = mlab.window_none(self.sig_ones)
        assert_array_equal(res, self.sig_ones)
