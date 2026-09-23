@pytest.mark.parametrize('width, height', [
    (1, np.nan),
    (-1, 1),
    (np.inf, 1)
])
def test_invalid_figure_size(width, height):
    with pytest.raises(ValueError):
        plt.figure(figsize=(width, height))

    fig = plt.figure()
    with pytest.raises(ValueError):
        fig.set_size_inches(width, height)
