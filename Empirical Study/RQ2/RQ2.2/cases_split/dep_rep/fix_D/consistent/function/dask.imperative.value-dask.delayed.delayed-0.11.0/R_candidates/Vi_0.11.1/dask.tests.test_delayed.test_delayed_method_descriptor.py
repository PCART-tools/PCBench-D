def test_delayed_method_descriptor():
    delayed(bytes.decode)(b'')  # does not err
