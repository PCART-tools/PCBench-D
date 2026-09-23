@pytest.mark.skipif("not bokeh")
@pytest.mark.skipif("not psutil")
def test_resource_profiler_plot():
    with ResourceProfiler(dt=0.01) as rprof:
        get(dsk2, 'c')
    p = rprof.visualize(plot_width=500,
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
    rprof.clear()
    rprof.visualize(show=False, save=False)
