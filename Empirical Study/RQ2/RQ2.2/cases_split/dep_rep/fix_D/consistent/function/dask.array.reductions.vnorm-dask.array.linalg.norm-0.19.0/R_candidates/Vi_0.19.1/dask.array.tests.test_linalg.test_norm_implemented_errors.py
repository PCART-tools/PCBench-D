@pytest.mark.parametrize("shape, chunks, axis", [
    [(3, 2, 4), (2, 2, 2), (1, 2)],
    [(2, 3, 4, 5), (2, 2, 2, 2), (-1, -2)],
])
@pytest.mark.parametrize("norm", [
    "nuc",
    2,
    -2
])
@pytest.mark.parametrize("keepdims", [
    False,
    True,
])
def test_norm_implemented_errors(shape, chunks, axis, norm, keepdims):
    a = np.random.random(shape)
    d = da.from_array(a, chunks=chunks)
    if len(shape) > 2 and len(axis) == 2:
        with pytest.raises(NotImplementedError):
            da.linalg.norm(d, ord=norm, axis=axis, keepdims=keepdims)
