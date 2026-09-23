def test_key_names_include_type_names():
    assert delayed(1).key.startswith('int')
