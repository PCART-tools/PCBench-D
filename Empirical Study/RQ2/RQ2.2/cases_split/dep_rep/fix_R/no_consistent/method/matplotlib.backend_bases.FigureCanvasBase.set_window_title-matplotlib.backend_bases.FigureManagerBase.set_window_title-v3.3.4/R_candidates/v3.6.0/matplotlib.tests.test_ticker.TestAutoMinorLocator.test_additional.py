    @pytest.mark.parametrize('lim, ref', additional_data)
    def test_additional(self, lim, ref):
        fig, ax = plt.subplots()

        ax.minorticks_on()
        ax.grid(True, 'minor', 'y', linewidth=1)
        ax.grid(True, 'major', color='k', linewidth=1)
        ax.set_ylim(lim)

        assert_almost_equal(ax.yaxis.get_ticklocs(minor=True), ref)
