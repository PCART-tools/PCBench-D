@image_comparison(['bxp_custompatchartist.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 100},
                  style='default')
def test_bxp_custompatchartist():
    _bxp_test_helper(bxp_kwargs=dict(
        patch_artist=True,
        boxprops=dict(facecolor='yellow', edgecolor='green', ls=':')))
