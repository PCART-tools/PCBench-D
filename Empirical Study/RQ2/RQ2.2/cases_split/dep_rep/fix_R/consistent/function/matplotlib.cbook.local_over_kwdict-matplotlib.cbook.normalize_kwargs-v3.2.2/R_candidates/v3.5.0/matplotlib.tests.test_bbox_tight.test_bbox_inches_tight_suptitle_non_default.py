@image_comparison(['bbox_inches_tight_suptile_non_default.png'],
                  remove_text=False, savefig_kwarg={'bbox_inches': 'tight'},
                  tol=0.1)  # large tolerance because only testing clipping.
def test_bbox_inches_tight_suptitle_non_default():
    fig, ax = plt.subplots()
    fig.suptitle('Booo', x=0.5, y=1.1)
