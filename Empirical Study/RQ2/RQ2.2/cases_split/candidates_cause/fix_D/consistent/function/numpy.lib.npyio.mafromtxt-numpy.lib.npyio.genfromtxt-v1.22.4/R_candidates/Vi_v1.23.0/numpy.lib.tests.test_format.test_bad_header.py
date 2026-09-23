def test_bad_header():
    # header of length less than 2 should fail
    s = BytesIO()
    assert_raises(ValueError, format.read_array_header_1_0, s)
    s = BytesIO(b'1')
    assert_raises(ValueError, format.read_array_header_1_0, s)

    # header shorter than indicated size should fail
    s = BytesIO(b'\x01\x00')
    assert_raises(ValueError, format.read_array_header_1_0, s)

    # headers without the exact keys required should fail
    d = {"shape": (1, 2),
         "descr": "x"}
    s = BytesIO()
    format.write_array_header_1_0(s, d)
    assert_raises(ValueError, format.read_array_header_1_0, s)

    d = {"shape": (1, 2),
         "fortran_order": False,
         "descr": "x",
         "extrakey": -1}
    s = BytesIO()
    format.write_array_header_1_0(s, d)
    assert_raises(ValueError, format.read_array_header_1_0, s)
