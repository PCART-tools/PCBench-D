@pytest.mark.parametrize("funcname", [
    "atleast_1d",
    "atleast_2d",
    "atleast_3d",
])
@pytest.mark.parametrize("shape1, shape2", list(
    itertools.combinations_with_replacement(
        [
            tuple(),
            (4,),
            (4, 6),
            (4, 6, 8),
            (4, 6, 8, 10),
        ],
        2
    )
))
def test_atleast_nd_two_args(funcname, shape1, shape2):
    np_a_1 = np.random.random(shape1)
    da_a_1 = da.from_array(np_a_1, chunks=tuple(c // 2 for c in shape1))

    np_a_2 = np.random.random(shape2)
    da_a_2 = da.from_array(np_a_2, chunks=tuple(c // 2 for c in shape2))

    np_a_n = [np_a_1, np_a_2]
    da_a_n = [da_a_1, da_a_2]

    np_func = getattr(np, funcname)
    da_func = getattr(da, funcname)

    np_r_n = np_func(*np_a_n)
    da_r_n = da_func(*da_a_n)

    assert type(np_r_n) is type(da_r_n)

    assert len(np_r_n) == len(da_r_n)

    for np_r, da_r in zip(np_r_n, da_r_n):
        assert_eq(np_r, da_r)
