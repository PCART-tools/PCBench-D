    def test_window_none_ones(self):
        res = mlab.window_none(self.sig_rand)
        assert_array_equal(res, self.sig_rand)
