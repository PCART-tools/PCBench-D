@check_figures_equal(extensions=["png"])
def test_invisible_axes(fig_test, fig_ref):
    ax = fig_test.subplots(subplot_kw=dict(projection='3d'))
    ax.set_visible(False)
