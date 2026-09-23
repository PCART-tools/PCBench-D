    def test_fail_list_of_str(self):
        with pytest.raises(ValueError, match='must be 2D'):
            plt.subplot_mosaic(['foo', 'bar'])
        with pytest.raises(ValueError, match='must be 2D'):
            plt.subplot_mosaic(['foo'])
        with pytest.raises(ValueError, match='must be 2D'):
            plt.subplot_mosaic([['foo', ('bar',)]])
        with pytest.raises(ValueError, match='must be 2D'):
            plt.subplot_mosaic([['a', 'b'], [('a', 'b'), 'c']])
