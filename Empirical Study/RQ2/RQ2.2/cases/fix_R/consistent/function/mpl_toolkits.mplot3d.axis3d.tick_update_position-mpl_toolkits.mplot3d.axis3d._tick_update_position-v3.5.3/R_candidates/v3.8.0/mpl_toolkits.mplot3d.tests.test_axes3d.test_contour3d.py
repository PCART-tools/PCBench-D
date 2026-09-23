@mpl3d_image_comparison(
    ['contour3d.png'], style='mpl20',
    tol=0.002 if platform.machine() in ('aarch64', 'ppc64le', 's390x') else 0)
def test_contour3d():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)
    ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
    ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
    ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
    ax.axis(xmin=-40, xmax=40, ymin=-40, ymax=40, zmin=-100, zmax=100)
