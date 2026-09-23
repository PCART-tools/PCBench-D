def test_raises():
    for ver in ['1.9', '1,9.0', '1.7.x']:
        assert_raises(ValueError, NumpyVersion, ver)
