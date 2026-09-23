def test_free_symbols():
    assert (C*D).free_symbols == {C, D}
