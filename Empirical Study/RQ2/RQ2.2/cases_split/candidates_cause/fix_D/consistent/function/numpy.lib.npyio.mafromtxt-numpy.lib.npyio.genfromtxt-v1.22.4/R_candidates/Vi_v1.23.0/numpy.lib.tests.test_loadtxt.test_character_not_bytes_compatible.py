@pytest.mark.skipif(IS_PYPY and sys.implementation.version <= (7, 3, 8),
                    reason="PyPy bug in error formatting")
def test_character_not_bytes_compatible():
    """Test exception when a character cannot be encoded as 'S'."""
    data = StringIO("–")  # == \u2013
    with pytest.raises(ValueError):
        np.loadtxt(data, dtype="S5")
