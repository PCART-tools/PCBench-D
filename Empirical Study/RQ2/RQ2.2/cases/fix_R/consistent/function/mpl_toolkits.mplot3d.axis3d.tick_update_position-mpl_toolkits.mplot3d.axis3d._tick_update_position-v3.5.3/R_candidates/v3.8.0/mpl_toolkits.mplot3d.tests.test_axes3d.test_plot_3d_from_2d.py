@mpl3d_image_comparison(['plot_3d_from_2d.png'], tol=0.015, style='mpl20')
def test_plot_3d_from_2d():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    xs = np.arange(0, 5)
    ys = np.arange(5, 10)
    ax.plot(xs, ys, zs=0, zdir='x')
    ax.plot(xs, ys, zs=0, zdir='y')
