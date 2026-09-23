@mpl3d_image_comparison(['tricontour.png'], tol=0.02, style='mpl20')
def test_tricontour():
    fig = plt.figure()

    np.random.seed(19680801)
    x = np.random.rand(1000) - 0.5
    y = np.random.rand(1000) - 0.5
    z = -(x**2 + y**2)

    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.tricontour(x, y, z)
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.tricontourf(x, y, z)
