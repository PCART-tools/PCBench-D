def test_adjoining_partitions():
    p1 = nn.Sequential(StashFoo())
    p2 = nn.Sequential(PopFoo())

    layout = inspect_skip_layout([p1, p2])
    policy = [list(layout.copy_policy(i)) for i in range(2)]

    assert policy == [[], [(0, None, "foo")]]
