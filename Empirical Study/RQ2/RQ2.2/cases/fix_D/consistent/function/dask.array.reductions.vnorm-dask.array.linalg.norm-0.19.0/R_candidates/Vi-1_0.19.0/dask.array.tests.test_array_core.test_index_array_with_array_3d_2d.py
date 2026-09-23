@pytest.mark.xfail(reason='Chunking does not align well')
def test_index_array_with_array_3d_2d():
    x = np.arange(4**3).reshape((4, 4, 4))
    dx = da.from_array(x, chunks=(2, 2, 2))

    ind = np.random.random((4, 4)) > 0.5
    ind = np.arange(4 ** 2).reshape((4, 4)) % 2 == 0
    dind = da.from_array(ind, (2, 2))

    assert_eq(x[ind], dx[dind])
    assert_eq(x[:, ind], dx[:, dind])
