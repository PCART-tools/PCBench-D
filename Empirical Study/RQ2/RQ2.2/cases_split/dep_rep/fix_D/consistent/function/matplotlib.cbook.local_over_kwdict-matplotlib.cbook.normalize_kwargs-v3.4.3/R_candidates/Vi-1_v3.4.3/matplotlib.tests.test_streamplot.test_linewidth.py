@image_comparison(['streamplot_linewidth'], remove_text=True, style='mpl20')
def test_linewidth():
    X, Y, U, V = velocity_field()
    speed = np.hypot(U, V)
    lw = 5 * speed / speed.max()
    # Compatibility for old test image
    df = 25 / 30
    ax = plt.figure().subplots()
    ax.set(xlim=(-3.0, 2.9999999999999947),
           ylim=(-3.0000000000000004, 2.9999999999999947))
    ax.streamplot(X, Y, U, V, density=[0.5 * df, 1. * df], color='k',
                  linewidth=lw)
