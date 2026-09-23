def test_tree_reduce_set_options():
    x = da.from_array(np.arange(242).reshape((11, 22)), chunks=(3, 4))
    with set_options(split_every={0: 2, 1: 3}):
        assert_max_deps(x.sum(), 2 * 3)
        assert_max_deps(x.sum(axis=0), 2)
