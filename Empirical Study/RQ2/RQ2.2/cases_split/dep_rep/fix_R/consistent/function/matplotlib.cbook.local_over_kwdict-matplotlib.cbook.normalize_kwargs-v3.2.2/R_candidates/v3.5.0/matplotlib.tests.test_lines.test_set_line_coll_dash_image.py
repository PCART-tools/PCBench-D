@image_comparison(['line_collection_dashes'], remove_text=True, style='mpl20')
def test_set_line_coll_dash_image():
    fig, ax = plt.subplots()
    np.random.seed(0)
    ax.contour(np.random.randn(20, 30), linestyles=[(0, (3, 3))])
