@pytest.mark.parametrize('selector', ['span', 'rectangle'])
def test_selector_clear(selector):
    ax = get_ax()

    def onselect(*args):
        pass

    kwargs = dict(ax=ax, onselect=onselect, interactive=True)
    if selector == 'span':
        Selector = widgets.SpanSelector
        kwargs['direction'] = 'horizontal'
    else:
        Selector = widgets.RectangleSelector

    tool = Selector(**kwargs)
    do_event(tool, 'press', xdata=10, ydata=10, button=1)
    do_event(tool, 'onmove', xdata=100, ydata=120, button=1)
    do_event(tool, 'release', xdata=100, ydata=120, button=1)

    # press-release event outside the selector to clear the selector
    do_event(tool, 'press', xdata=130, ydata=130, button=1)
    do_event(tool, 'release', xdata=130, ydata=130, button=1)
    assert not tool._selection_completed

    ax = get_ax()
    kwargs['ignore_event_outside'] = True
    tool = Selector(**kwargs)
    assert tool.ignore_event_outside
    do_event(tool, 'press', xdata=10, ydata=10, button=1)
    do_event(tool, 'onmove', xdata=100, ydata=120, button=1)
    do_event(tool, 'release', xdata=100, ydata=120, button=1)

    # press-release event outside the selector ignored
    do_event(tool, 'press', xdata=130, ydata=130, button=1)
    do_event(tool, 'release', xdata=130, ydata=130, button=1)
    assert tool._selection_completed

    do_event(tool, 'on_key_press', key='escape')
    assert not tool._selection_completed
