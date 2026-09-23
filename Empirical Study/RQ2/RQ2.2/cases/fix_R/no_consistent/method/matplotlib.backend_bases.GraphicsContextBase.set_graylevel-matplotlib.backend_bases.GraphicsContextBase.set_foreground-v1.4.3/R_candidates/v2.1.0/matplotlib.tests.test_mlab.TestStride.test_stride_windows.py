    @pytest.mark.parametrize('axis', [0, 1], ids=['axis0', 'axis1'])
    @pytest.mark.parametrize('n, noverlap',
                             [(1, 0), (5, 0), (15, 2), (13, -3)],
                             ids=['n1-noverlap0', 'n5-noverlap0',
                                  'n15-noverlap2', 'n13-noverlapn3'])
    def test_stride_windows(self, n, noverlap, axis):
        x = np.arange(100)
        y = mlab.stride_windows(x, n, noverlap=noverlap, axis=axis)

        expected_shape = [0, 0]
        expected_shape[axis] = n
        expected_shape[1 - axis] = 100 // (n - noverlap)
        yt = self.calc_window_target(x, n, noverlap=noverlap, axis=axis)

        assert yt.shape == y.shape
        assert_array_equal(yt, y)
        assert tuple(expected_shape) == y.shape
        assert self.get_base(y) is x
