def test_contourf_legend_elements():
    x, y = np.mgrid[1:10, 1:10]
    h = x * y

    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    cs = ax.contourf(x, y, h, levels=[10, 30, 50],
                     colors=['#FFFF00', '#FF00FF', '#00FFFF'],
                     extend='both')
    cs.cmap.set_over('red')
    cs.cmap.set_under('blue')
    cs.changed()
    artists, labels = cs.legend_elements()
    assert labels == ['$x \\leq -1e+250s$',
                      '$10.0 < x \\leq 30.0$',
                      '$30.0 < x \\leq 50.0$',
                      '$x > 1e+250s$']
    expected_colors = ('blue', '#FFFF00', '#FF00FF', 'red')
    assert all(isinstance(a, mpl.patches.Rectangle) for a in artists)
    assert all(same_color(a.get_facecolor(), c)
               for a, c in zip(artists, expected_colors))
