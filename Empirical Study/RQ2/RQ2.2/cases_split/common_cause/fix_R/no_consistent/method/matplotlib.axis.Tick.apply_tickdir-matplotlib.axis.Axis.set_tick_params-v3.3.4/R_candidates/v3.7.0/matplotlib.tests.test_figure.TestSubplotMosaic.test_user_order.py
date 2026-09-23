    @pytest.mark.parametrize('str_pattern',
                             ['abc', 'cab', 'bca', 'cba', 'acb', 'bac'])
    def test_user_order(self, str_pattern):
        fig = plt.figure()
        ax_dict = fig.subplot_mosaic(str_pattern)
        assert list(str_pattern) == list(ax_dict)
        assert list(fig.axes) == list(ax_dict.values())
