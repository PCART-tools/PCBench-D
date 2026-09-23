@pytest.mark.parametrize('data', [[[]], [[], [0, 1]], [[0, 1], []]])
@pytest.mark.parametrize(
    'orientation', ['_empty', 'vertical', 'horizontal', None, 'none'])
def test_eventplot_orientation(data, orientation):
    """Introduced when fixing issue #6412."""
    opts = {} if orientation == "_empty" else {'orientation': orientation}
    fig, ax = plt.subplots(1, 1)
    with (pytest.warns(MatplotlibDeprecationWarning)
          if orientation in [None, 'none'] else nullcontext()):
        ax.eventplot(data, **opts)
    plt.draw()
