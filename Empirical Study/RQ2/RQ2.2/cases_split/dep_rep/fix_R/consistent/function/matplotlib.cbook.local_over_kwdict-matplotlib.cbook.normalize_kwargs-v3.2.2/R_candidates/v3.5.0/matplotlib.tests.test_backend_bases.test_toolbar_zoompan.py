def test_toolbar_zoompan():
    expected_warning_regex = (
        r"Treat the new Tool classes introduced in "
        r"v[0-9]*.[0-9]* as experimental for now; "
        "the API and rcParam may change in future versions.")
    with pytest.warns(UserWarning, match=expected_warning_regex):
        plt.rcParams['toolbar'] = 'toolmanager'
    ax = plt.gca()
    assert ax.get_navigate_mode() is None
    ax.figure.canvas.manager.toolmanager.add_tool(name="zoom",
                                                  tool=ToolZoom)
    ax.figure.canvas.manager.toolmanager.add_tool(name="pan",
                                                  tool=ToolPan)
    ax.figure.canvas.manager.toolmanager.add_tool(name=_views_positions,
                                                  tool=ToolViewsPositions)
    ax.figure.canvas.manager.toolmanager.add_tool(name='rubberband',
                                                  tool=RubberbandBase)
    ax.figure.canvas.manager.toolmanager.trigger_tool('zoom')
    assert ax.get_navigate_mode() == "ZOOM"
    ax.figure.canvas.manager.toolmanager.trigger_tool('pan')
    assert ax.get_navigate_mode() == "PAN"
