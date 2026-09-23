@image_comparison(['regularpolycollection_rotate.png'], remove_text=True)
def test_regularpolycollection_rotate():
    xx, yy = np.mgrid[:10, :10]
    xy_points = np.transpose([xx.flatten(), yy.flatten()])
    rotations = np.linspace(0, 2*np.pi, len(xy_points))

    fig, ax = plt.subplots()
    for xy, alpha in zip(xy_points, rotations):
        col = mcollections.RegularPolyCollection(
            4, sizes=(100,), rotation=alpha,
            offsets=[xy], transOffset=ax.transData)
        ax.add_collection(col, autolim=True)
    ax.autoscale_view()
