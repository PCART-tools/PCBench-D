@image_comparison(['streamplot_linewidth'], remove_text=True, style='mpl20',
                  tol=0.002)
def test_linewidth():
    X, Y, U, V = velocity_field()
    speed = np.hypot(U, V)
    lw = 5 * speed / speed.max()
    ax = plt.figure().subplots()
    ax.streamplot(X, Y, U, V, density=[0.5, 1], color='k', linewidth=lw)
