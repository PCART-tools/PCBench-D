@image_comparison(['skew_axes'], remove_text=True)
def test_set_line_coll_dash_image():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='skewx')
    ax.set_xlim(-50, 50)
    ax.set_ylim(50, -50)
    ax.grid(True)

    # An example of a slanted line at constant X
    ax.axvline(0, color='b')
