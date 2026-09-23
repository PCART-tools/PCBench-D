def test_literal_serializable():
    l = literal((add, 1, 2))
    assert pickle.loads(pickle.dumps(l)).data == (add, 1, 2)
