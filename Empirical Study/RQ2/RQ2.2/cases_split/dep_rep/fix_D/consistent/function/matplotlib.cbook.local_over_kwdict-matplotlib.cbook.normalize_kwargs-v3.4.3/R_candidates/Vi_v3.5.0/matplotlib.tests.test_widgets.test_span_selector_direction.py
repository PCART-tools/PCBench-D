def test_span_selector_direction():
    ax = get_ax()

    def onselect(*args):
        pass

    tool = widgets.SpanSelector(ax, onselect, 'horizontal', interactive=True)
    assert tool.direction == 'horizontal'
    assert tool._edge_handles.direction == 'horizontal'

    with pytest.raises(ValueError):
        tool = widgets.SpanSelector(ax, onselect, 'invalid_direction')

    tool.direction = 'vertical'
    assert tool.direction == 'vertical'
    assert tool._edge_handles.direction == 'vertical'

    with pytest.raises(ValueError):
        tool.direction = 'invalid_string'
