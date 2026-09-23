@pytest.mark.skipif("not bokeh")
def test_cache_profiler_plot():
    with CacheProfiler(metric_name='non-standard') as cprof:
        get(dsk, 'e')
    p = cprof.visualize(plot_width=500,
                        plot_height=300,
                        tools="hover",
                        title="Not the default",
                        show=False, save=False)
    assert p.plot_width == 500
    assert p.plot_height == 300
    assert len(p.tools) == 1
    assert isinstance(p.tools[0], bokeh.models.HoverTool)
    assert check_title(p, "Not the default")
    assert p.axis[1].axis_label == 'Cache Size (non-standard)'
    # Test empty, checking for errors
    cprof.clear()
    cprof.visualize(show=False, save=False)
