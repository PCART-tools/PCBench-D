@image_comparison(['violinplot_horiz_showmedians.png'])
def test_horiz_violinplot_showmedians():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(23))
    np.random.seed(795831523)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), vert=False, showmeans=0,
                  showextrema=0, showmedians=1)
