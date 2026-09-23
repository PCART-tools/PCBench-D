def test_free_symbols():
    assert PropertiesOnlyMatrix([[x], [0]]).free_symbols == {x}
