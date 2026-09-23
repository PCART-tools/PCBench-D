@check_figures_equal(extensions=["png"])
def test_remove_cb_whose_mappable_has_no_figure(fig_ref, fig_test):
    ax = fig_test.add_subplot()
    cb = fig_test.colorbar(cm.ScalarMappable(), cax=ax)
    cb.remove()
