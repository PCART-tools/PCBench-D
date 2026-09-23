def test_rectangle_selector_set_props_handle_props():
    ax = get_ax()

    def onselect(epress, erelease):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True,
                                     props=dict(facecolor='b', alpha=0.2),
                                     handle_props=dict(alpha=0.5))
    # Create rectangle
    do_event(tool, 'press', xdata=0, ydata=10, button=1)
    do_event(tool, 'onmove', xdata=100, ydata=120, button=1)
    do_event(tool, 'release', xdata=100, ydata=120, button=1)

    artist = tool._selection_artist
    assert artist.get_facecolor() == mcolors.to_rgba('b', alpha=0.2)
    tool.set_props(facecolor='r', alpha=0.3)
    assert artist.get_facecolor() == mcolors.to_rgba('r', alpha=0.3)

    for artist in tool._handles_artists:
        assert artist.get_markeredgecolor() == 'black'
        assert artist.get_alpha() == 0.5
    tool.set_handle_props(markeredgecolor='r', alpha=0.3)
    for artist in tool._handles_artists:
        assert artist.get_markeredgecolor() == 'r'
        assert artist.get_alpha() == 0.3
