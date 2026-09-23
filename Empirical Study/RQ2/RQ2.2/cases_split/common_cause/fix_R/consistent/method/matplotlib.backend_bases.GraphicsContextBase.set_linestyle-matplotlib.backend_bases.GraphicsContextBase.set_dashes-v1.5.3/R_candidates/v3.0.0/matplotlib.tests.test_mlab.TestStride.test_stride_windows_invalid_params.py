    @pytest.mark.parametrize('n, noverlap',
                             [(0, None), (11, None), (2, 2), (2, 3)],
                             ids=['n less than 1', 'n greater than input',
                                  'noverlap greater than n',
                                  'noverlap equal to n'])
    def test_stride_windows_invalid_params(self, n, noverlap):
        x = np.arange(10)
        with pytest.raises(ValueError):
            mlab.stride_windows(x, n, noverlap)
