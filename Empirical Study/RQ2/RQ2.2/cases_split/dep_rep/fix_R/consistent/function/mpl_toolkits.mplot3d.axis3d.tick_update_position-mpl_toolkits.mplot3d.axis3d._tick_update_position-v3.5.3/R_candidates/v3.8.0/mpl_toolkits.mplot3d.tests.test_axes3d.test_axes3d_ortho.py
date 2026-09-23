@mpl3d_image_comparison(['axes3d_ortho.png'], remove_text=False, style='mpl20')
def test_axes3d_ortho():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_proj_type('ortho')
