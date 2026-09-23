@mpl3d_image_comparison(['grid_off.png'], style='mpl20')
def test_grid_off():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.grid(False)
