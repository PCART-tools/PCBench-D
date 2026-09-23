def test_pop_2_from_different_partitions():
    p1 = nn.Sequential(StashFoo())
    p2 = nn.Sequential(StashBar())
    p3 = nn.Sequential(PopBar(), PopFoo())

    layout = inspect_skip_layout([p1, p2, p3])
    policy = [list(layout.copy_policy(i)) for i in range(3)]

    # p3 pops 'bar' before 'foo', but the plan is sorted by source partition index.
    assert policy == [[], [], [(0, None, "foo"), (1, None, "bar")]]
