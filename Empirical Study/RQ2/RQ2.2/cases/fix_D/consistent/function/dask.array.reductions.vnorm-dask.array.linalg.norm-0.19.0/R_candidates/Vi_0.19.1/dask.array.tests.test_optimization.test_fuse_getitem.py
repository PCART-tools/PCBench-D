def test_fuse_getitem():
    pairs = [((getter, (getter, 'x', slice(1000, 2000)), slice(15, 20)),
              (getter, 'x', slice(1015, 1020))),

             ((getitem, (getter, 'x', (slice(1000, 2000), slice(100, 200))),
                        (slice(15, 20), slice(50, 60))),
              (getter, 'x', (slice(1015, 1020), slice(150, 160)))),

             ((getitem, (getter_nofancy, 'x', (slice(1000, 2000), slice(100, 200))),
                        (slice(15, 20), slice(50, 60))),
              (getter_nofancy, 'x', (slice(1015, 1020), slice(150, 160)))),

             ((getter, (getter, 'x', slice(1000, 2000)), 10),
              (getter, 'x', 1010)),

             ((getitem, (getter, 'x', (slice(1000, 2000), 10)),
                        (slice(15, 20),)),
              (getter, 'x', (slice(1015, 1020), 10))),

             ((getitem, (getter_nofancy, 'x', (slice(1000, 2000), 10)),
                        (slice(15, 20),)),
              (getter_nofancy, 'x', (slice(1015, 1020), 10))),

             ((getter, (getter, 'x', (10, slice(1000, 2000))),
               (slice(15, 20), )),
              (getter, 'x', (10, slice(1015, 1020)))),

             ((getter, (getter, 'x', (slice(1000, 2000), slice(100, 200))),
               (slice(None, None), slice(50, 60))),
              (getter, 'x', (slice(1000, 2000), slice(150, 160)))),

             ((getter, (getter, 'x', (None, slice(None, None))),
               (slice(None, None), 5)),
              (getter, 'x', (None, 5))),

             ((getter, (getter, 'x', (slice(1000, 2000), slice(10, 20))),
               (slice(5, 10),)),
              (getter, 'x', (slice(1005, 1010), slice(10, 20)))),

             ((getitem, (getitem, 'x', (slice(1000, 2000),)),
               (slice(5, 10), slice(10, 20))),
              (getitem, 'x', (slice(1005, 1010), slice(10, 20)))),

             ((getter, (getter, 'x', slice(1000, 2000), False, False), slice(15, 20)),
              (getter, 'x', slice(1015, 1020))),

             ((getter, (getter, 'x', slice(1000, 2000)), slice(15, 20), False, False),
              (getter, 'x', slice(1015, 1020))),

             ((getter, (getter_nofancy, 'x', slice(1000, 2000), False, False),
               slice(15, 20), False, False),
              (getter_nofancy, 'x', slice(1015, 1020), False, False)),
             ]

    for inp, expected in pairs:
        result = optimize_slices({'y': inp})
        assert result == {'y': expected}
