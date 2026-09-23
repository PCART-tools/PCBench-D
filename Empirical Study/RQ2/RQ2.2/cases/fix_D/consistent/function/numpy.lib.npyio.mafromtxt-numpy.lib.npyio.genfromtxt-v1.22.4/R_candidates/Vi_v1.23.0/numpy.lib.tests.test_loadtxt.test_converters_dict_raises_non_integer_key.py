@pytest.mark.skipif(IS_PYPY and sys.implementation.version <= (7, 3, 8),
                    reason="PyPy bug in error formatting")
def test_converters_dict_raises_non_integer_key():
    with pytest.raises(TypeError, match="keys of the converters dict"):
        np.loadtxt(StringIO("1 2\n3 4"), converters={"a": int})
    with pytest.raises(TypeError, match="keys of the converters dict"):
        np.loadtxt(StringIO("1 2\n3 4"), converters={"a": int}, usecols=0)
