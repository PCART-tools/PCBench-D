@pytest.mark.parametrize('data', [[[]], [[], [0, 1]], [[0, 1], []]])
@pytest.mark.parametrize('orientation', [None, 'vertical', 'horizontal'])
def test_eventplot_orientation(data, orientation):
    """Introduced when fixing issue #6412."""
    opts = {} if orientation is None else {'orientation': orientation}
    fig, ax = plt.subplots(1, 1)
    ax.eventplot(data, **opts)
    plt.draw()
