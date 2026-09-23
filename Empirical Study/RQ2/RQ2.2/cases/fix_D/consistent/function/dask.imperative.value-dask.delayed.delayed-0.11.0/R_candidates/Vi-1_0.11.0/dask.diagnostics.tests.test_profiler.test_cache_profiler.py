def test_cache_profiler():
    with CacheProfiler() as cprof:
        get(dsk2, 'c')
    results = cprof.results
    assert all(isinstance(i, tuple) and len(i) == 5 for i in results)

    cprof.clear()
    assert cprof.results == []

    tics = [0]
    def nbytes(res):
        tics[0] += 1
        return tics[0]

    with CacheProfiler(nbytes) as cprof:
        get(dsk2, 'c')
    results = cprof.results
    assert tics[-1] == len(results)
    assert tics[-1] == results[-1].metric
    assert cprof._metric_name == 'nbytes'
    assert CacheProfiler(metric=nbytes, metric_name='foo')._metric_name == 'foo'
