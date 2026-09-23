@pytest.mark.style('default')
def test_warn_ignored_scatter_kwargs():
    with pytest.warns(UserWarning,
                      match=r"You passed a edgecolor/edgecolors"):

        c = plt.scatter(
            [0], [0], marker="+", s=500, facecolor="r", edgecolor="b"
        )
