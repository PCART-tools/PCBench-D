@check_figures_equal(extensions=['png'])
def test_stairs_baseline_0(fig_test, fig_ref):
    # Test
    test_ax = fig_test.add_subplot()
    test_ax.stairs([5, 6, 7], baseline=None)

    # Ref
    ref_ax = fig_ref.add_subplot()
    style = {'solid_joinstyle': 'miter', 'solid_capstyle': 'butt'}
    ref_ax.plot(range(4), [5, 6, 7, 7], drawstyle='steps-post', **style)
    ref_ax.set_ylim(0, None)
