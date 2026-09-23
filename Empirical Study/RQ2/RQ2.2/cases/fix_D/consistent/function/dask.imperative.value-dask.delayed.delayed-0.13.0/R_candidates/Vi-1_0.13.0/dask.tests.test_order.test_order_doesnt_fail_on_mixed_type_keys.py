def test_order_doesnt_fail_on_mixed_type_keys():
    order({'x': (inc, 1),
           ('y', 0): (inc, 2),
           'z': (add, 'x', ('y', 0))})
