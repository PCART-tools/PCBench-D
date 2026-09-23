@pytest.mark.parametrize("toolbar", ["none", "toolbar2", "toolmanager"])
def test_TextBox(toolbar):
    # Avoid "toolmanager is provisional" warning.
    dict.__setitem__(plt.rcParams, "toolbar", toolbar)

    from unittest.mock import Mock
    submit_event = Mock()
    text_change_event = Mock()
    ax = get_ax()
    tool = widgets.TextBox(ax, '')
    tool.on_submit(submit_event)
    tool.on_text_change(text_change_event)

    assert tool.text == ''

    do_event(tool, '_click')

    tool.set_val('x**2')

    assert tool.text == 'x**2'
    assert text_change_event.call_count == 1

    tool.begin_typing(tool.text)
    tool.stop_typing()

    assert submit_event.call_count == 2

    do_event(tool, '_click')
    do_event(tool, '_keypress', key='+')
    do_event(tool, '_keypress', key='5')

    assert text_change_event.call_count == 3
