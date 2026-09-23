    @pytest.mark.parametrize('unicode_minus, result',
                             [(True, "\N{MINUS SIGN}1"), (False, "-1")])
    def test_unicode_minus(self, unicode_minus, result):
        mpl.rcParams['axes.unicode_minus'] = unicode_minus
        assert (
            plt.gca().xaxis.get_major_formatter().format_data_short(-1).strip()
            == result)
