def test_agm_simple():
    assert_allclose(special.agm(24, 6), 13.4581714817)
    assert_allclose(special.agm(1e30, 1), 2.2292230559453832047768593e28)
