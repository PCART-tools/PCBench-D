def test_far_partitions():
    p1 = nn.Sequential(StashFoo())
    p2 = nn.Sequential(Pass())
    p3 = nn.Sequential(PopFoo())

    layout = inspect_skip_layout([p1, p2, p3])
    policy = [list(layout.copy_policy(i)) for i in range(3)]

    assert policy == [[], [], [(0, None, "foo")]]
