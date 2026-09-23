def test_einsum_broadcasting_contraction3():
    a = np.random.rand(1, 5, 4)
    b = np.random.rand(4, 1, 6)
    c = np.random.rand(5, 6)
    d = np.random.rand(7, 7)

    d_a = da.from_array(a, chunks=(1, (2, 3), (2, 2)))
    d_b = da.from_array(b, chunks=((2, 2), 1,  (4, 2)))
    d_c = da.from_array(c, chunks=((2, 3), (4, 2)))
    d_d = da.from_array(d, chunks=((7, 3)))

    np_res = np.einsum('ajk,kbl,jl,ab->ab', a, b, c, d)
    da_res = da.einsum('ajk,kbl,jl,ab->ab', d_a, d_b, d_c, d_d)
    assert_eq(np_res, da_res)
