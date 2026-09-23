def test_namespace():
    ns1 = Namespace()
    ns2 = Namespace()

    p1 = nn.Sequential(StashFoo().isolate(ns1))
    p2 = nn.Sequential(StashFoo().isolate(ns2))
    p3 = nn.Sequential(PopFoo().isolate(ns2), PopFoo().isolate(ns1))

    layout = inspect_skip_layout([p1, p2, p3])
    policy = [list(layout.copy_policy(i)) for i in range(3)]

    # p3 pops 'bar' before 'foo', but the plan is sorted by source partition index.
    assert policy == [[], [], [(0, ns1, "foo"), (1, ns2, "foo")]]
