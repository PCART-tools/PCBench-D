def test_warn_external(recwarn):
    _api.warn_external("oops")
    assert len(recwarn) == 1
    assert recwarn[0].filename == __file__
