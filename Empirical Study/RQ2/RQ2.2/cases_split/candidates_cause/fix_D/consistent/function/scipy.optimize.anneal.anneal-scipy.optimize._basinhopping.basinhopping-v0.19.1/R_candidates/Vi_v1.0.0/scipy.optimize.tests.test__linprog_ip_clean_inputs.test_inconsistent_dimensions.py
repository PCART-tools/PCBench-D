def test_inconsistent_dimensions():
    m = 2
    n = 4
    c = [1, 2, 3, 4]

    Agood = np.random.rand(m, n)
    Abad = np.random.rand(m, n + 1)
    bgood = np.random.rand(m)
    bbad = np.random.rand(m + 1)
    boundsbad = [(0, 1)] * (n + 1)
    assert_raises(ValueError, _clean_inputs, c=c, A_ub=Abad, b_ub=bgood)
    assert_raises(ValueError, _clean_inputs, c=c, A_ub=Agood, b_ub=bbad)
    assert_raises(ValueError, _clean_inputs, c=c, A_eq=Abad, b_eq=bgood)
    assert_raises(ValueError, _clean_inputs, c=c, A_eq=Agood, b_eq=bbad)
    assert_raises(ValueError, _clean_inputs, c=c, bounds=boundsbad)
