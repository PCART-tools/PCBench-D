@pytest.mark.skipif("not bokeh")
def test_profiler_plot():
    with prof:
        get(dsk, 'e')
    p = prof.visualize(plot_width=500,
                       plot_height=300,
                       tools="hover",
                       title="Not the default",
                       show=False, save=False)
    assert p.plot_width == 500
    assert p.plot_height == 300
    assert len(p.tools) == 1
    assert isinstance(p.tools[0], bokeh.models.HoverTool)
    assert check_title(p, "Not the default")
    # Test empty, checking for errors
    prof.clear()
    prof.visualize(show=False, save=False)
