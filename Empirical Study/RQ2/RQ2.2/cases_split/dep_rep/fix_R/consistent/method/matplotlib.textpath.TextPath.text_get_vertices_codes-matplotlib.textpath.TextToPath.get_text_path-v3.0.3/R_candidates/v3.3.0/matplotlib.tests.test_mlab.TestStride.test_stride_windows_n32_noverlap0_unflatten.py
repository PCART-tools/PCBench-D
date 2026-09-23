    @pytest.mark.parametrize('axis', [0, 1], ids=['axis0', 'axis1'])
    def test_stride_windows_n32_noverlap0_unflatten(self, axis):
        n = 32
        x = np.arange(n)[np.newaxis]
        x1 = np.tile(x, (21, 1))
        x2 = x1.flatten()
        y = mlab.stride_windows(x2, n, axis=axis)

        if axis == 0:
            x1 = x1.T
        assert y.shape == x1.shape
        assert_array_equal(y, x1)
