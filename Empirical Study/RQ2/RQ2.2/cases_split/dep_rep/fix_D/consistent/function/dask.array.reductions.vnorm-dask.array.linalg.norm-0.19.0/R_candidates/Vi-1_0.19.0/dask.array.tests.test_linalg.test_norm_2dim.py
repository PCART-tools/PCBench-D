@pytest.mark.parametrize("shape, chunks, axis", [
    [(5, 6), (2, 2), None],
    [(5, 6), (2, 2), (0, 1)],
    [(5, 6), (2, 2), (1, 0)],
])
@pytest.mark.parametrize("norm", [
    "fro",
    "nuc",
    2,
    -2
])
@pytest.mark.parametrize("keepdims", [
    False,
    True,
])
def test_norm_2dim(shape, chunks, axis, norm, keepdims):
    a = np.random.random(shape)
    d = da.from_array(a, chunks=chunks)

    # Need one chunk on last dimension for svd.
    if norm == "nuc" or norm == 2 or norm == -2:
        d = d.rechunk((d.chunks[0], d.shape[1]))

    a_r = np.linalg.norm(a, ord=norm, axis=axis, keepdims=keepdims)
    d_r = da.linalg.norm(d, ord=norm, axis=axis, keepdims=keepdims)

    assert_eq(a_r, d_r)
