@image_comparison([
    'EventCollection_plot__set_linestyle',
    'EventCollection_plot__set_linestyle',
    'EventCollection_plot__set_linewidth',
])
def test__EventCollection__set_prop():
    for prop, value, expected in [
            ('linestyle', 'dashed', [(0, (6.0, 6.0))]),
            ('linestyle', (0, (6., 6.)), [(0, (6.0, 6.0))]),
            ('linewidth', 5, 5),
    ]:
        splt, coll, _ = generate_EventCollection_plot()
        coll.set(**{prop: value})
        assert plt.getp(coll, prop) == expected
        splt.set_title(f'EventCollection: set_{prop}')
