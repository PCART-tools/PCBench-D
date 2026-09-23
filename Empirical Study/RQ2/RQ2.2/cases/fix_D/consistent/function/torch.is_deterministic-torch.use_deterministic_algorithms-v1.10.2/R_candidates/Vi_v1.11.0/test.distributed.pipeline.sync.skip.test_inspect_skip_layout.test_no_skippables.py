def test_no_skippables():
    p1 = nn.Sequential(Pass())
    p2 = nn.Sequential(Pass())

    layout = inspect_skip_layout([p1, p2])
    policy = [list(layout.copy_policy(i)) for i in range(2)]

    assert policy == [[], []]
