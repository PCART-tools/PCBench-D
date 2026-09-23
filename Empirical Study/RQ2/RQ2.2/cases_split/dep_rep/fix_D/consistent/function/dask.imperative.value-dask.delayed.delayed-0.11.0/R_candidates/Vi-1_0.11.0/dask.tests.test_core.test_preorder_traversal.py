def test_preorder_traversal():
    t = (add, 1, 2)
    assert list(preorder_traversal(t)) == [add, 1, 2]
    t = (add, (add, 1, 2), (add, 3, 4))
    assert list(preorder_traversal(t)) == [add, add, 1, 2, add, 3, 4]
    t = (add, (sum, [1, 2]), 3)
    assert list(preorder_traversal(t)) == [add, sum, list, 1, 2, 3]
