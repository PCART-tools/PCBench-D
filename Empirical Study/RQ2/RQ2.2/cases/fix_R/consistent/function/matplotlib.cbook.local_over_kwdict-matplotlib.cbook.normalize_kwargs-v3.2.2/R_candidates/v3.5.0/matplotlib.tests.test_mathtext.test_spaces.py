@check_figures_equal(extensions=["png"])
def test_spaces(fig_test, fig_ref):
    fig_test.subplots().set_title(r"$1\,2\>3\ 4$")
    fig_ref.subplots().set_title(r"$1\/2\:3~4$")
