@check_figures_equal(extensions=["png"])
def test_imshow_norm_vminvmax(fig_test, fig_ref):
    """Parameters vmin, vmax should be ignored if norm is given."""
    a = [[1, 2], [3, 4]]
    ax = fig_ref.subplots()
    ax.imshow(a, vmin=0, vmax=5)
    ax = fig_test.subplots()
    with pytest.warns(MatplotlibDeprecationWarning,
                      match="Passing parameters norm and vmin/vmax "
                            "simultaneously is deprecated."):
        ax.imshow(a, norm=mcolors.Normalize(-10, 10), vmin=0, vmax=5)
