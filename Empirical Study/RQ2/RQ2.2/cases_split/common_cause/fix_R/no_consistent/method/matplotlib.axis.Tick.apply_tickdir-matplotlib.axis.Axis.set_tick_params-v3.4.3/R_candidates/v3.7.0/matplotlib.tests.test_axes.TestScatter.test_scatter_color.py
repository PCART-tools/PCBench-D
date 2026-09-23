    def test_scatter_color(self):
        # Try to catch cases where 'c' kwarg should have been used.
        with pytest.raises(ValueError):
            plt.scatter([1, 2], [1, 2], color=[0.1, 0.2])
        with pytest.raises(ValueError):
            plt.scatter([1, 2, 3], [1, 2, 3], color=[1, 2, 3])
