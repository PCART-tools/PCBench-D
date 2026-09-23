@pytest.mark.skipif(IS_PYPY and sys.implementation.version <= (7, 3, 8),
                    reason="PyPy bug in error formatting")
@pytest.mark.parametrize("dtype",
            np.typecodes["AllInteger"] + "efgdFDG" + "?")
def test_nul_character_error(dtype):
    # Test that a \0 character is correctly recognized as an error even if
    # what comes before is valid (not everything gets parsed internally).
    if dtype.lower() == "g":
        pytest.xfail("longdouble/clongdouble assignment may misbehave.")
    with pytest.raises(ValueError):
        np.loadtxt(["1\000"], dtype=dtype, delimiter=",", quotechar='"')
