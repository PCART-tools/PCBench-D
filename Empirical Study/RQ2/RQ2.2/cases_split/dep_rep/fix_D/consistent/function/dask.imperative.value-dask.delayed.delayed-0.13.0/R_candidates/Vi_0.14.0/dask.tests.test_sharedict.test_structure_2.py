@pytest.mark.skip
def test_structure_2():
    s = ShareDict()
    s.update_with_key(a, key='a')
    s.update_with_key(b, key='b')
    s.update_with_key(c, key='c')

    assert s.order == ['a', 'b', 'c']

    s.update_with_key(b, key='b')

    assert s.order == ['a', 'c', 'b']
