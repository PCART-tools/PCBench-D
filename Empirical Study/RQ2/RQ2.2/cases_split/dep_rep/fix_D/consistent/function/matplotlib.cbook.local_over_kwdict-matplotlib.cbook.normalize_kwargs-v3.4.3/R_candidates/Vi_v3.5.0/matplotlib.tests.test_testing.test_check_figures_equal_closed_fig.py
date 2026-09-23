@check_figures_equal()
def test_check_figures_equal_closed_fig(fig_test, fig_ref):
    fig = plt.figure()
    plt.close(fig)
