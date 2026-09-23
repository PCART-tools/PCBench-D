def test_vindex_errors():
    d = da.ones((5, 5, 5), chunks=(3, 3, 3))
    pytest.raises(IndexError, lambda: d.vindex[np.newaxis])
    pytest.raises(IndexError, lambda: d.vindex[[1, 2], [1, 2, 3]])
    pytest.raises(IndexError, lambda: d.vindex[[True] * 5])
    pytest.raises(IndexError, lambda: d.vindex[[0], [5]])
    pytest.raises(IndexError, lambda: d.vindex[[0], [-6]])
