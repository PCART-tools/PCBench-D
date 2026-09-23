@pytest.mark.skipif(IS_PYPY and sys.implementation.version <= (7, 3, 8),
                    reason="PyPy bug in error formatting")
@pytest.mark.parametrize("dtype", np.typecodes["AllInteger"])
@pytest.mark.filterwarnings("error:.*integer via a float.*:DeprecationWarning")
def test_integer_signs(dtype):
    dtype = np.dtype(dtype)
    assert np.loadtxt(["+2"], dtype=dtype) == 2
    if dtype.kind == "u":
        with pytest.raises(ValueError):
            np.loadtxt(["-1\n"], dtype=dtype)
    else:
        assert np.loadtxt(["-2\n"], dtype=dtype) == -2

    for sign in ["++", "+-", "--", "-+"]:
        with pytest.raises(ValueError):
            np.loadtxt([f"{sign}2\n"], dtype=dtype)
