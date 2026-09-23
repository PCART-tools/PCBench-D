def _assert_records_equal(actual, ref):
    assert isinstance(actual, Field)
    assert isinstance(ref, Field)
    b1 = actual.field_blobs()
    b2 = ref.field_blobs()
    assert len(b1) == len(b2), "Records have different lengths: %d vs. %d" % (
        len(b1),
        len(b2),
    )
    for name, d1, d2 in zip(ref.field_names(), b1, b2):
        _assert_arrays_equal(d1, d2, err_msg="Mismatch in field %s." % name)
