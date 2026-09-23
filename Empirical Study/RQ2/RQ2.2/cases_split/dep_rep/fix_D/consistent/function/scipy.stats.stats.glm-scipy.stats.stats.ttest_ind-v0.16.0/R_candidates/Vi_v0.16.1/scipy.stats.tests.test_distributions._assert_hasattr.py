def _assert_hasattr(a, b, msg=None):
    if msg is None:
        msg = '%s does not have attribute %s' % (a, b)
    assert_(hasattr(a, b), msg=msg)
