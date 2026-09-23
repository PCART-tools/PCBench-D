@image_comparison(['test_bbox.png'],
                  remove_text=True, style='mpl20',
                  savefig_kwarg={'bbox_inches':
                                 mtransforms.Bbox([[0.5, 0], [2.5, 2]])})
def test_bbox():
    fig, ax = plt.subplots(constrained_layout=True)
    ax.set_aspect(1.)
