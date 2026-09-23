@image_comparison(['marker_styles.png'], remove_text=True)
def test_marker_styles():
    fig, ax = plt.subplots()
    for y, marker in enumerate(sorted(matplotlib.markers.MarkerStyle.markers,
                                      key=lambda x: str(type(x))+str(x))):
        ax.plot((y % 2)*5 + np.arange(10)*10, np.ones(10)*10*y, linestyle='',
                marker=marker, markersize=10+y/5, label=marker)
