    @pytest.mark.parametrize('axis', [-1, 2],
                             ids=['axis less than 0',
                                  'axis greater than input shape'])
    def test_stride_repeat_invalid_axis(self, axis):
        x = np.array(0)
        with pytest.raises(ValueError):
            mlab.stride_repeat(x, 5, axis=axis)
