def test_reduction_names():
    x = da.ones(5, chunks=(2,))
    assert x.sum().name.startswith('sum')
    assert 'max' in x.max().name.split('-')[0]
    assert x.var().name.startswith('var')
    assert x.all().name.startswith('all')
    assert any(k[0].startswith('nansum') for k in da.nansum(x).dask)
    assert x.mean().name.startswith('mean')
