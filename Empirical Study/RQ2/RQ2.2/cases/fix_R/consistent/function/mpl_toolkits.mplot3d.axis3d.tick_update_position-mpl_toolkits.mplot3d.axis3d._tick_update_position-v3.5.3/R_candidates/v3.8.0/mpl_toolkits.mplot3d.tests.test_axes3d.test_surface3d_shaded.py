@mpl3d_image_comparison(['surface3d_shaded.png'], style='mpl20')
def test_surface3d_shaded():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R)
    ax.plot_surface(X, Y, Z, rstride=5, cstride=5,
                    color=[0.25, 1, 0.25], lw=1, antialiased=False)
    ax.set_zlim(-1.01, 1.01)
