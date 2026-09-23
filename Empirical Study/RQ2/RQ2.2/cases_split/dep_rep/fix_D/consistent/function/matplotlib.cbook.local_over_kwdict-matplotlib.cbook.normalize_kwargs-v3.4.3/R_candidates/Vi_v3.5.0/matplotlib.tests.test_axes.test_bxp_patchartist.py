@image_comparison(['bxp_patchartist.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_patchartist():
    _bxp_test_helper(bxp_kwargs=dict(patch_artist=True))
