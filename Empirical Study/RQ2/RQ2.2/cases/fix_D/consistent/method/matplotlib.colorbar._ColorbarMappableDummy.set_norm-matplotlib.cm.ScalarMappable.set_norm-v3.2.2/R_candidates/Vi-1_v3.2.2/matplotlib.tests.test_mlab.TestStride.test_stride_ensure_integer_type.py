    def test_stride_ensure_integer_type(self):
        N = 100
        x = np.full(N + 20, np.nan)
        y = x[10:-10]
        y[:] = 0.3
        # previous to #3845 lead to corrupt access
        y_strided = mlab.stride_windows(y, n=33, noverlap=0.6)
        assert_array_equal(y_strided, 0.3)
        # previous to #3845 lead to corrupt access
        y_strided = mlab.stride_windows(y, n=33.3, noverlap=0)
        assert_array_equal(y_strided, 0.3)
        # even previous to #3845 could not find any problematic
        # configuration however, let's be sure it's not accidentally
        # introduced
        y_strided = _stride_repeat(y, n=33.815)
        assert_array_equal(y_strided, 0.3)
