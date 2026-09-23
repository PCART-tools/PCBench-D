@pytest.mark.parametrize("return_index", [False, True])
@pytest.mark.parametrize("return_inverse", [False, True])
@pytest.mark.parametrize("return_counts", [False, True])
def test_unique_kwargs(return_index, return_inverse, return_counts):
    kwargs = dict(
        return_index=return_index,
        return_inverse=return_inverse,
        return_counts=return_counts
    )

    a = np.array([1, 2, 4, 4, 5, 2])
    d = da.from_array(a, chunks=(3,))

    r_a = np.unique(a, **kwargs)
    r_d = da.unique(d, **kwargs)

    if not any([return_index, return_inverse, return_counts]):
        assert isinstance(r_a, np.ndarray)
        assert isinstance(r_d, da.Array)

        r_a = (r_a,)
        r_d = (r_d,)

    assert len(r_a) == len(r_d)

    if return_inverse:
        i = 1 + int(return_index)
        assert (d.size,) == r_d[i].shape

    for e_r_a, e_r_d in zip(r_a, r_d):
        assert_eq(e_r_d, e_r_a)
