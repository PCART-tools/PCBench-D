@image_comparison(['collection'], tol=0.03, style='mpl20')
def test_collection():
    x, y = np.meshgrid(np.linspace(0, 10, 150), np.linspace(-5, 5, 100))
    data = np.sin(x) + np.cos(y)
    cs = plt.contour(data)
    pe = [path_effects.PathPatchEffect(edgecolor='black', facecolor='none',
                                       linewidth=12),
          path_effects.Stroke(linewidth=5)]

    for collection in cs.collections:
        collection.set_path_effects(pe)

    for text in plt.clabel(cs, colors='white'):
        text.set_path_effects([path_effects.withStroke(foreground='k',
                                                       linewidth=3)])
        text.set_bbox({'boxstyle': 'sawtooth', 'facecolor': 'none',
                       'edgecolor': 'blue'})
