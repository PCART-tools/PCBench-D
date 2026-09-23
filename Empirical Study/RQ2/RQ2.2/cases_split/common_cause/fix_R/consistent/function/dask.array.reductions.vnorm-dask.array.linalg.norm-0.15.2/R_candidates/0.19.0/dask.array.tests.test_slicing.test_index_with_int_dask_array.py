@pytest.mark.parametrize('idx_chunks', [None, 3, 2, 1])
@pytest.mark.parametrize('x_chunks', [None, (3, 5), (2, 3), (1, 2), (1, 1)])
def test_index_with_int_dask_array(x_chunks, idx_chunks):
    # test data is crafted to stress use cases:
    # - pick from different chunks of x out of order
    # - a chunk of x contains no matches
    # - only one chunk of x
    x = np.array([[10, 20, 30, 40, 50],
                  [60, 70, 80, 90, 100],
                  [110, 120, 130, 140, 150]])
    idx = np.array([3, 0, 1])
    expect = np.array([[40, 10, 20],
                       [90, 60, 70],
                       [140, 110, 120]])

    if x_chunks is not None:
        x = da.from_array(x, chunks=x_chunks)
    if idx_chunks is not None:
        idx = da.from_array(idx, chunks=idx_chunks)

    assert_eq(x[:, idx], expect)
    assert_eq(x.T[idx, :], expect.T)
