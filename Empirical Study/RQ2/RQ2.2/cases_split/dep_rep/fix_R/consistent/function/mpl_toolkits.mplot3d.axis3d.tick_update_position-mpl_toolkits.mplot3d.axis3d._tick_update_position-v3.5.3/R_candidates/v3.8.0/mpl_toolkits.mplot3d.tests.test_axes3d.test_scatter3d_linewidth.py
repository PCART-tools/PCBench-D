@mpl3d_image_comparison(['scatter3d_linewidth.png'], style='mpl20')
def test_scatter3d_linewidth():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Check that array-like linewidth can be set
    ax.scatter(np.arange(10), np.arange(10), np.arange(10),
               marker='o', linewidth=np.arange(10))
