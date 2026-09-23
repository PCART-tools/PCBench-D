@mpl3d_image_comparison(['surface3d.png'], style='mpl20')
def test_surface3d():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.hypot(X, Y)
    Z = np.sin(R)
    surf = ax.plot_surface(X, Y, Z, rcount=40, ccount=40, cmap=cm.coolwarm,
                           lw=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)
    fig.colorbar(surf, shrink=0.5, aspect=5)
