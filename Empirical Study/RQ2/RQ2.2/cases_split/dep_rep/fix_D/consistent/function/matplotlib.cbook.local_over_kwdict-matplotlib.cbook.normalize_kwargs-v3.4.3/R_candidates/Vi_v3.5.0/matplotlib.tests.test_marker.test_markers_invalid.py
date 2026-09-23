@pytest.mark.parametrize('marker', [
    'square',  # arbitrary string
    np.array([[-0.5, 0, 1, 2, 3]]),  # 1D array
    (1,),
    (5, 3),  # second parameter of tuple must be 0, 1, or 2
    (1, 2, 3, 4),
])
def test_markers_invalid(marker):
    with pytest.raises(ValueError):
        markers.MarkerStyle(marker)
