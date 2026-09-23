@image_comparison(['tickedstroke'], remove_text=True, extensions=['png'],
                  tol=0.22)  # Increased tolerance due to fixed clipping.
def test_tickedstroke():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
    path = Path.unit_circle()
    patch = patches.PathPatch(path, facecolor='none', lw=2, path_effects=[
        path_effects.withTickedStroke(angle=-90, spacing=10,
                                      length=1)])

    ax1.add_patch(patch)
    ax1.axis('equal')
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)

    ax2.plot([0, 1], [0, 1], label=' ',
             path_effects=[path_effects.withTickedStroke(spacing=7,
                                                         angle=135)])
    nx = 101
    x = np.linspace(0.0, 1.0, nx)
    y = 0.3 * np.sin(x * 8) + 0.4
    ax2.plot(x, y, label=' ', path_effects=[path_effects.withTickedStroke()])

    ax2.legend()

    nx = 101
    ny = 105

    # Set up survey vectors
    xvec = np.linspace(0.001, 4.0, nx)
    yvec = np.linspace(0.001, 4.0, ny)

    # Set up survey matrices.  Design disk loading and gear ratio.
    x1, x2 = np.meshgrid(xvec, yvec)

    # Evaluate some stuff to plot
    g1 = -(3 * x1 + x2 - 5.5)
    g2 = -(x1 + 2 * x2 - 4)
    g3 = .8 + x1 ** -3 - x2

    cg1 = ax3.contour(x1, x2, g1, [0], colors=('k',))
    plt.setp(cg1.collections,
             path_effects=[path_effects.withTickedStroke(angle=135)])

    cg2 = ax3.contour(x1, x2, g2, [0], colors=('r',))
    plt.setp(cg2.collections,
             path_effects=[path_effects.withTickedStroke(angle=60, length=2)])

    cg3 = ax3.contour(x1, x2, g3, [0], colors=('b',))
    plt.setp(cg3.collections,
             path_effects=[path_effects.withTickedStroke(spacing=7)])

    ax3.set_xlim(0, 4)
    ax3.set_ylim(0, 4)
