@pytest.mark.parametrize('shape,chunks', [[(4,), (2,)],
                                          [(4, 4), (2, 2)],
                                          [(4, 4), (4, 2)]])
def test_dont_concatenate_single_chunks(shape, chunks):
    x = da.ones(shape, chunks=shape)
    y = x.rechunk(chunks)
    dsk = dict(y.dask)
    assert not any(funcname(task[0]).startswith('concat')
                   for task in dsk.values()
                   if dask.istask(task))
