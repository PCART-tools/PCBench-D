@image_comparison(['violinplot_horiz_custompoints_200.png'])
def test_horiz_violinplot_custompoints_200():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(43))
    np.random.seed(557438524)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), vert=False, showmeans=0,
                  showextrema=0, showmedians=0, points=200)
