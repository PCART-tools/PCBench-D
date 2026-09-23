def test_full_invalid():
    fig, ax = plt.subplots()
    ax.imshow(np.full((10, 10), np.nan))
    with pytest.warns(UserWarning):
        fig.canvas.draw()
