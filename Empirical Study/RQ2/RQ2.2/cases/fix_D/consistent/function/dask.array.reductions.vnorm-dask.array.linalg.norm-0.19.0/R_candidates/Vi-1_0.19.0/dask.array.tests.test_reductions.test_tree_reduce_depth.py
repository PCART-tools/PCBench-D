def test_tree_reduce_depth():
    # 2D
    x = da.from_array(np.arange(242).reshape((11, 22)), chunks=(3, 4))
    thresh = {0: 2, 1: 3}
    assert_max_deps(x.sum(split_every=thresh), 2 * 3)
    assert_max_deps(x.sum(axis=0, split_every=thresh), 2)
    assert_max_deps(x.sum(axis=1, split_every=thresh), 3)
    assert_max_deps(x.sum(split_every=20), 20, False)
    assert_max_deps(x.sum(axis=0, split_every=20), 4)
    assert_max_deps(x.sum(axis=1, split_every=20), 6)

    # 3D
    x = da.from_array(np.arange(11 * 22 * 29).reshape((11, 22, 29)), chunks=(3, 4, 5))
    thresh = {0: 2, 1: 3, 2: 4}
    assert_max_deps(x.sum(split_every=thresh), 2 * 3 * 4)
    assert_max_deps(x.sum(axis=0, split_every=thresh), 2)
    assert_max_deps(x.sum(axis=1, split_every=thresh), 3)
    assert_max_deps(x.sum(axis=2, split_every=thresh), 4)
    assert_max_deps(x.sum(axis=(0, 1), split_every=thresh), 2 * 3)
    assert_max_deps(x.sum(axis=(0, 2), split_every=thresh), 2 * 4)
    assert_max_deps(x.sum(axis=(1, 2), split_every=thresh), 3 * 4)
    assert_max_deps(x.sum(split_every=20), 20, False)
    assert_max_deps(x.sum(axis=0, split_every=20), 4)
    assert_max_deps(x.sum(axis=1, split_every=20), 6)
    assert_max_deps(x.sum(axis=2, split_every=20), 6)
    assert_max_deps(x.sum(axis=(0, 1), split_every=20), 20, False)
    assert_max_deps(x.sum(axis=(0, 2), split_every=20), 20, False)
    assert_max_deps(x.sum(axis=(1, 2), split_every=20), 20, False)
    assert_max_deps(x.sum(axis=(0, 1), split_every=40), 4 * 6)
    assert_max_deps(x.sum(axis=(0, 2), split_every=40), 4 * 6)
    assert_max_deps(x.sum(axis=(1, 2), split_every=40), 6 * 6)
