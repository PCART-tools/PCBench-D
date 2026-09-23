def draw_quiver(ax, **kw):
    X, Y = np.meshgrid(np.arange(0, 2 * np.pi, 1),
                       np.arange(0, 2 * np.pi, 1))
    U = np.cos(X)
    V = np.sin(Y)

    Q = ax.quiver(U, V, **kw)
    return Q
