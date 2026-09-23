def test_different_seeds():
    seed = 37
    state = np.random.RandomState(seed)
    n = 100000

    # Use an integer
    seeds = set(different_seeds(n, seed))
    assert len(seeds) == n

    # Use RandomState object
    seeds2 = set(different_seeds(n, state))
    assert seeds == seeds2

    # Should be sorted
    smallseeds = different_seeds(10, 1234)
    assert smallseeds == sorted(smallseeds)
