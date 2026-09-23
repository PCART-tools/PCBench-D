def test_marker_as_markerstyle():
    fix, ax = plt.subplots()
    m = mmarkers.MarkerStyle('o')
    ax.plot([1, 2, 3], [3, 2, 1], marker=m)
    ax.scatter([1, 2, 3], [4, 3, 2], marker=m)
    ax.errorbar([1, 2, 3], [5, 4, 3], marker=m)
