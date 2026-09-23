@image_comparison(['streamplot_startpoints'], remove_text=True, style='mpl20',
                  tol=0.513)
def test_startpoints():
    X, Y, U, V = velocity_field()
    start_x = np.linspace(X.min(), X.max(), 10)
    start_y = np.linspace(Y.min(), Y.max(), 10)
    start_points = np.column_stack([start_x, start_y])
    plt.streamplot(X, Y, U, V, start_points=start_points)
    plt.plot(start_x, start_y, 'ok')
