@pytest.mark.skipif("not bokeh")
def test_get_colors():
    from dask.diagnostics.profile_visualize import get_colors
    from bokeh.palettes import Blues9, Blues5, Viridis
    from itertools import cycle
    funcs = list(range(11))
    cmap = get_colors('Blues', funcs)
    lk = dict(zip(funcs, cycle(Blues9)))
    assert cmap == [lk[i] for i in funcs]

    funcs = list(range(5))
    cmap = get_colors('Blues', funcs)
    lk = dict(zip(funcs, Blues5))
    assert cmap == [lk[i] for i in funcs]

    funcs = [0, 1, 0, 1, 0, 1]
    cmap = get_colors('BrBG', funcs)
    assert len(set(cmap)) == 2

    funcs = list(range(100))
    cmap = get_colors('Viridis', funcs)
    assert len(set(cmap)) == 100

    funcs = list(range(300))
    cmap = get_colors('Viridis', funcs)
    assert len(set(cmap)) == len(set(Viridis[256]))
