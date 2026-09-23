def test_fuse_getitem_lock():
    lock1 = SerializableLock()
    lock2 = SerializableLock()

    pairs = [((getter, (getter, 'x', slice(1000, 2000), True, lock1), slice(15, 20)),
              (getter, 'x', slice(1015, 1020), True, lock1)),

             ((getitem, (getter, 'x', (slice(1000, 2000), slice(100, 200)), True, lock1),
                        (slice(15, 20), slice(50, 60))),
              (getter, 'x', (slice(1015, 1020), slice(150, 160)), True, lock1)),

             ((getitem, (getter_nofancy, 'x', (slice(1000, 2000), slice(100, 200)), True, lock1),
                        (slice(15, 20), slice(50, 60))),
              (getter_nofancy, 'x', (slice(1015, 1020), slice(150, 160)), True, lock1)),

             ((getter, (getter, 'x', slice(1000, 2000), True, lock1), slice(15, 20), True, lock2),
              (getter, (getter, 'x', slice(1000, 2000), True, lock1), slice(15, 20), True, lock2))]

    for inp, expected in pairs:
        result = optimize_slices({'y': inp})
        assert result == {'y': expected}
