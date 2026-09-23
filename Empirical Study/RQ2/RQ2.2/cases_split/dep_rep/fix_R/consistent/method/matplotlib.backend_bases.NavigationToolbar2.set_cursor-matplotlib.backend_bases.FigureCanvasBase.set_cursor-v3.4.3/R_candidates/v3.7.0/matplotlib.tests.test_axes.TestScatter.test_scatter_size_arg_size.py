    def test_scatter_size_arg_size(self):
        x = np.arange(4)
        with pytest.raises(ValueError, match='same size as x and y'):
            plt.scatter(x, x, x[1:])
        with pytest.raises(ValueError, match='same size as x and y'):
            plt.scatter(x[1:], x[1:], x)
        with pytest.raises(ValueError, match='float array-like'):
            plt.scatter(x, x, 'foo')
