    @pytest.mark.parametrize('nb_majorticks, expected_nb_minorticks', params)
    def test_low_number_of_majorticks(
            self, nb_majorticks, expected_nb_minorticks):
        # This test is related to issue #8804
        fig, ax = plt.subplots()
        xlims = (0, 5)  # easier to test the different code paths
        ax.set_xlim(*xlims)
        ax.set_xticks(np.linspace(xlims[0], xlims[1], nb_majorticks))
        ax.minorticks_on()
        ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
        assert len(ax.xaxis.get_minorticklocs()) == expected_nb_minorticks
