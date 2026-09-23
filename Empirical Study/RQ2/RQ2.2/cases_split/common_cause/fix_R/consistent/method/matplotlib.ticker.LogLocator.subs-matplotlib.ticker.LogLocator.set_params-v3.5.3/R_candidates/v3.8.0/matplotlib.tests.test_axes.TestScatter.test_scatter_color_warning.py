    @pytest.mark.parametrize('kwargs',
                                [
                                    {'cmap': 'gray'},
                                    {'norm': mcolors.Normalize()},
                                    {'vmin': 0},
                                    {'vmax': 0}
                                ])
    def test_scatter_color_warning(self, kwargs):
        warn_match = "No data for colormapping provided "
        # Warn for cases where 'cmap', 'norm', 'vmin', 'vmax'
        # kwargs are being overridden
        with pytest.warns(Warning, match=warn_match):
            plt.scatter([], [], **kwargs)
        with pytest.warns(Warning, match=warn_match):
            plt.scatter([1, 2], [3, 4], c=[], **kwargs)
        # Do not warn for cases where 'c' matches 'x' and 'y'
        plt.scatter([], [], c=[], **kwargs)
        plt.scatter([1, 2], [3, 4], c=[4, 5], **kwargs)
