@pytest.mark.skipif("not psutil")
def test_resource_profiler():
    with ResourceProfiler(dt=0.01) as rprof:
        get(dsk2, 'c')
    results = rprof.results
    assert all(isinstance(i, tuple) and len(i) == 3 for i in results)

    rprof.clear()
    assert rprof.results == []

    rprof.close()
    assert not rprof._tracker.is_alive()

    with pytest.raises(AssertionError):
        with rprof:
            get(dsk, 'e')
