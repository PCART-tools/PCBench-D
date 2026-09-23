@check_figures_equal()
def test_empty(fig_test, fig_ref):
    mpl.rcParams['text.usetex'] = True
    fig_test.text(.5, .5, "% a comment")
