    def test_stride_repeat_n_lt_1_ValueError(self):
        x = np.arange(10)
        with pytest.raises(ValueError):
            _stride_repeat(x, 0)
