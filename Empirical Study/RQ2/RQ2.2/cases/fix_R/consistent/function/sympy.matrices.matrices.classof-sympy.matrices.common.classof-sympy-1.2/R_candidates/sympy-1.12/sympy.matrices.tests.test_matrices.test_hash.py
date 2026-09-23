def test_hash():
    for cls in classes[-2:]:
        s = {cls.eye(1), cls.eye(1)}
        assert len(s) == 1 and s.pop() == cls.eye(1)
    # issue 3979
    for cls in classes[:2]:
        assert not isinstance(cls.eye(1), Hashable)
