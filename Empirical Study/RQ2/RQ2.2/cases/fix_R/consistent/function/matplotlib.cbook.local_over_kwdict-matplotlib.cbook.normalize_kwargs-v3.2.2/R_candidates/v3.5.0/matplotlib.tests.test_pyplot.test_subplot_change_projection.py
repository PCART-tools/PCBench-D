def test_subplot_change_projection():
    ax = plt.subplot()
    projections = ('aitoff', 'hammer', 'lambert', 'mollweide',
                   'polar', 'rectilinear', '3d')
    for proj in projections:
        ax_next = plt.subplot(projection=proj)
        assert ax_next is plt.subplot()
        assert ax_next.name == proj
        assert ax is not ax_next
        ax = ax_next
