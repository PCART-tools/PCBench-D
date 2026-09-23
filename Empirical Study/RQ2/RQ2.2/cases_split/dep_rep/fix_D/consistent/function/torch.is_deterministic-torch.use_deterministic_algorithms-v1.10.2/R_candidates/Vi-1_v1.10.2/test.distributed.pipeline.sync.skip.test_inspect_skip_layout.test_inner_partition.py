def test_inner_partition():
    p1 = nn.Sequential(StashFoo(), PopFoo())
    p2 = nn.Sequential(Pass())

    layout = inspect_skip_layout([p1, p2])
    policy = [list(layout.copy_policy(i)) for i in range(2)]

    assert policy == [[], []]
