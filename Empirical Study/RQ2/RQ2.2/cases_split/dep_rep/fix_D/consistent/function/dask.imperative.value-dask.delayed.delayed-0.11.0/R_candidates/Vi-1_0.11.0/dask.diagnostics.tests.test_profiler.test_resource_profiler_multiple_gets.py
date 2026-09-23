@pytest.mark.skipif("not psutil")
def test_resource_profiler_multiple_gets():
    with ResourceProfiler(dt=0.01) as rprof:
        get(dsk2, 'c')
        assert len(rprof.results) == 0
        get(dsk2, 'c')
    results = rprof.results
    assert all(isinstance(i, tuple) and len(i) == 3 for i in results)

    rprof.clear()
    rprof.register()
    get(dsk2, 'c')
    assert len(rprof.results) > 0
    get(dsk2, 'c')
    rprof.unregister()

    results = rprof.results
    assert all(isinstance(i, tuple) and len(i) == 3 for i in results)

    rprof.close()
    assert not rprof._tracker.is_alive()
