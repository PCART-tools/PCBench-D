@pytest.mark.parametrize("m,n", [
    (10, 20),
    (15, 15),
    (20, 10),
])
def test_dask_svd_self_consistent(m, n):
    a = np.random.rand(m, n)
    d_a = da.from_array(a, chunks=(3, n), name='A')

    d_u, d_s, d_vt = da.linalg.svd(d_a)
    u, s, vt = da.compute(d_u, d_s, d_vt)

    for d_e, e in zip([d_u, d_s, d_vt], [u, s, vt]):
        assert d_e.shape == e.shape
        assert d_e.dtype == e.dtype
