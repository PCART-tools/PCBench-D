def test_grouper_private():
    class Dummy:
        pass
    objs = [Dummy() for _ in range(5)]
    g = cbook.Grouper()
    g.join(*objs)
    # reach in and touch the internals !
    mapping = g._mapping

    for o in objs:
        assert ref(o) in mapping

    base_set = mapping[ref(objs[0])]
    for o in objs[1:]:
        assert mapping[ref(o)] is base_set
