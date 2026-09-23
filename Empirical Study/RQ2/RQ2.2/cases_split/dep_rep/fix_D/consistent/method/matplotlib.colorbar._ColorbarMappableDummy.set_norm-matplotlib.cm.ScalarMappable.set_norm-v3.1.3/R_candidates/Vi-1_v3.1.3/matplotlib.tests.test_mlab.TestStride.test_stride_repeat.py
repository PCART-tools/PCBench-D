    @pytest.mark.parametrize('axis', [0, 1], ids=['axis0', 'axis1'])
    @pytest.mark.parametrize('n', [1, 5], ids=['n1', 'n5'])
    def test_stride_repeat(self, n, axis):
        x = np.arange(10)
        y = mlab.stride_repeat(x, n, axis=axis)

        expected_shape = [10, 10]
        expected_shape[axis] = n
        yr = np.repeat(np.expand_dims(x, axis), n, axis=axis)

        assert yr.shape == y.shape
        assert_array_equal(yr, y)
        assert tuple(expected_shape) == y.shape
        assert self.get_base(y) is x
