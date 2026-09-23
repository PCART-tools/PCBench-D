@pytest.mark.parametrize('get,remove',
                         [(getter, False), (getter_nofancy, False), (getitem, True)])
def test_remove_no_op_slices_if_get_is_not_getter_or_getter_nofancy(get, remove):
    # Test that no-op slices are removed as long as get is not getter or
    # getter_nofancy. This ensures that `get` calls are always made in all
    # tasks created by `from_array`, even after optimization
    null = slice(0,None)
    opts = [((get, 'x', null, False, False),
             'x' if remove else (get, 'x', null, False, False)),
            ((getitem, (get, 'x', null, False, False), null),
             'x' if remove else (get, 'x', null, False, False)),
            ((getitem, (get, 'x', (null, null), False, False), ()),
             'x' if remove else (get, 'x', (null, null), False, False))]
    for orig, final in opts:
        assert optimize_slices({'a': orig}) == {'a': final}
