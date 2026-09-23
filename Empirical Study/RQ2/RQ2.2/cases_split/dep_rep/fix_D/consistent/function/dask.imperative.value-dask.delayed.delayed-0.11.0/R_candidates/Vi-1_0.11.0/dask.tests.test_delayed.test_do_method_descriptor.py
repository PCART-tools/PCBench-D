def test_do_method_descriptor():
    delayed(bytes.decode)(b'')  # does not err
