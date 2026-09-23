@pytest.mark.skipif("not bokeh")
@pytest.mark.skipif("not psutil")
def test_plot_multiple():
    from dask.diagnostics.profile_visualize import visualize
    with ResourceProfiler(dt=0.01) as rprof:
        with prof:
            get(dsk2, 'c')
    p = visualize([prof, rprof], label_size=50,
                  title="Not the default", show=False, save=False)
    if LooseVersion(bokeh.__version__) >= '0.12.0':
        figures = [r.children[0] for r in p.children[1].children]
    else:
        figures = [r[0] for r in p.children]
    assert len(figures) == 2
    assert check_title(figures[0], "Not the default")
    assert figures[0].xaxis[0].axis_label is None
    assert figures[1].title is None
    assert figures[1].xaxis[0].axis_label == 'Time (s)'
    # Test empty, checking for errors
    prof.clear()
    rprof.clear()
    visualize([prof, rprof], show=False, save=False)
