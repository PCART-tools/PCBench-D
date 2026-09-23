    @pytest.mark.parametrize('major_step, expected_nb_minordivisions',
                             majorstep_minordivisions)
    def test_number_of_minor_ticks(
            self, major_step, expected_nb_minordivisions):
        fig, ax = plt.subplots()
        xlims = (0, major_step)
        ax.set_xlim(*xlims)
        ax.set_xticks(xlims)
        ax.minorticks_on()
        ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
        nb_minor_divisions = len(ax.xaxis.get_minorticklocs()) + 1
        assert nb_minor_divisions == expected_nb_minordivisions
