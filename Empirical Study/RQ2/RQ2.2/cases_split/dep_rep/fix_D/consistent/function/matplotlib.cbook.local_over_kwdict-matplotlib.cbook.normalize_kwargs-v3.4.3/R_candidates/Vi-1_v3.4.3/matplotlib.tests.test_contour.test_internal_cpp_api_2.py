def test_internal_cpp_api_2():
    from matplotlib import _contour  # noqa: ensure lazy-loaded module *is* loaded.
    arr = [[0, 1], [2, 3]]
    qcg = mpl._contour.QuadContourGenerator(arr, arr, arr, None, True, 0)
    with pytest.raises(
            ValueError, match=r'filled contour levels must be increasing'):
        qcg.create_filled_contour(1, 0)
