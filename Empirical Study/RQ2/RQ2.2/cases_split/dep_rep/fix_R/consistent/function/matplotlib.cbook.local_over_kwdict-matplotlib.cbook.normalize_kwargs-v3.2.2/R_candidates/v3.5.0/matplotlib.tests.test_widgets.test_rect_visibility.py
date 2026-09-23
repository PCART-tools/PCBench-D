@check_figures_equal()
def test_rect_visibility(fig_test, fig_ref):
    # Check that requesting an invisible selector makes it invisible
    ax_test = fig_test.subplots()
    _ = fig_ref.subplots()

    def onselect(verts):
        pass

    tool = widgets.RectangleSelector(ax_test, onselect,
                                     props={'visible': False})
    tool.extents = (0.2, 0.8, 0.3, 0.7)
