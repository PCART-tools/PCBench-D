def test_get_dependencies_empty():
    dsk = {'x': (inc,)}
    assert get_dependencies(dsk, 'x') == set()
    assert get_dependencies(dsk, 'x', as_list=True) == []
