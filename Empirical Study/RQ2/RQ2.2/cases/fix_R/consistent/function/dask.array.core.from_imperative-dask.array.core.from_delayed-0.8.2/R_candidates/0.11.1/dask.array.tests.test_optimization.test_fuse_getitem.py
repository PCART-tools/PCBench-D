def test_fuse_getitem():
    pairs = [((getarray, (getarray, 'x', slice(1000, 2000)), slice(15, 20)),
              (getarray, 'x', slice(1015, 1020))),

             ((getitem, (getarray, 'x', (slice(1000, 2000), slice(100, 200))),
                        (slice(15, 20), slice(50, 60))),
              (getarray, 'x', (slice(1015, 1020), slice(150, 160)))),

             ((getitem, (getarray_nofancy, 'x', (slice(1000, 2000), slice(100, 200))),
                        (slice(15, 20), slice(50, 60))),
              (getarray_nofancy, 'x', (slice(1015, 1020), slice(150, 160)))),

             ((getarray, (getarray, 'x', slice(1000, 2000)), 10),
              (getarray, 'x', 1010)),

             ((getitem, (getarray, 'x', (slice(1000, 2000), 10)),
                        (slice(15, 20),)),
              (getarray, 'x', (slice(1015, 1020), 10))),

             ((getitem, (getarray_nofancy, 'x', (slice(1000, 2000), 10)),
                        (slice(15, 20),)),
              (getarray_nofancy, 'x', (slice(1015, 1020), 10))),

             ((getarray, (getarray, 'x', (10, slice(1000, 2000))),
                        (slice(15, 20),)),
              (getarray, 'x', (10, slice(1015, 1020)))),

             ((getarray, (getarray, 'x', (slice(1000, 2000), slice(100, 200))),
                        (slice(None, None), slice(50, 60))),
              (getarray, 'x', (slice(1000, 2000), slice(150, 160)))),

             ((getarray, (getarray, 'x', (None, slice(None, None))),
                        (slice(None, None), 5)),
              (getarray, 'x', (None, 5))),

             ((getarray, (getarray, 'x', (slice(1000, 2000), slice(10, 20))),
                        (slice(5, 10),)),
              (getarray, 'x', (slice(1005, 1010), slice(10, 20)))),

             ((getitem, (getitem, 'x', (slice(1000, 2000),)),
                        (slice(5, 10), slice(10, 20))),
              (getitem, 'x', (slice(1005, 1010), slice(10, 20))))
        ]

    for inp, expected in pairs:
        result = optimize_slices({'y': inp})
        assert result == {'y': expected}
