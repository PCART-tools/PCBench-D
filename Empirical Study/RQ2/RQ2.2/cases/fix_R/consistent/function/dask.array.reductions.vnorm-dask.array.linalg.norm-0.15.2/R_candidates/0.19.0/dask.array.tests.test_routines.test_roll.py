@pytest.mark.parametrize('chunks', [(4, 6), (2, 6)])
@pytest.mark.parametrize('shift', [3, 7, 9, (3, 9), (7, 2)])
@pytest.mark.parametrize('axis', [None, 0, 1, -1, (0, 1), (1, 0)])
def test_roll(chunks, shift, axis):
    x = np.random.randint(10, size=(4, 6))
    a = da.from_array(x, chunks=chunks)

    if _maybe_len(shift) != _maybe_len(axis):
        with pytest.raises(TypeError if axis is None else ValueError):
            da.roll(a, shift, axis)
    else:
        if (_maybe_len(shift) > 1 and
                LooseVersion(np.__version__) < LooseVersion("1.12.0")):
            pytest.skip(
                "NumPy %s doesn't support multiple axes with `roll`."
                " Need NumPy 1.12.0 or greater." % np.__version__
            )
        assert_eq(np.roll(x, shift, axis), da.roll(a, shift, axis))
