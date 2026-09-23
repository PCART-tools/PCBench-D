    @pytest.mark.parametrize(
        'sci_type, scilimits, lim, orderOfMag, fewticks', scilimits_data)
    def test_scilimits(self, sci_type, scilimits, lim, orderOfMag, fewticks):
        tmp_form = mticker.ScalarFormatter()
        tmp_form.set_scientific(sci_type)
        tmp_form.set_powerlimits(scilimits)
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(tmp_form)
        ax.set_ylim(*lim)
        if fewticks:
            ax.yaxis.set_major_locator(mticker.MaxNLocator(4))

        tmp_form.set_locs(ax.yaxis.get_majorticklocs())
        assert orderOfMag == tmp_form.orderOfMagnitude
