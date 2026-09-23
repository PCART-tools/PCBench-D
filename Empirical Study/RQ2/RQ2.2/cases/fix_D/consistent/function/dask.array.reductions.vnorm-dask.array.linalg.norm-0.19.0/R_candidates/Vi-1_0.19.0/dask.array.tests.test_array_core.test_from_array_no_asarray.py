@pytest.mark.parametrize('asarray,cls', [
    (True, np.ndarray),
    (False, np.matrix),
])
def test_from_array_no_asarray(asarray, cls):

    def assert_chunks_are_of_type(x):
        chunks = compute_as_if_collection(Array, x.dask, x.__dask_keys__())
        for c in concat(chunks):
            assert type(c) is cls

    x = np.matrix(np.arange(100).reshape((10, 10)))
    dx = da.from_array(x, chunks=(5, 5), asarray=asarray)
    assert_chunks_are_of_type(dx)
    assert_chunks_are_of_type(dx[0:5])
    assert_chunks_are_of_type(dx[0:5][:, 0])
