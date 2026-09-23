    @pytest.mark.parametrize('shape', [(), (10, 1)], ids=['0D', '2D'])
    def test_stride_repeat_invalid_input_shape(self, shape):
        x = np.arange(np.prod(shape)).reshape(shape)
        with pytest.raises(ValueError):
            mlab.stride_repeat(x, 5)
