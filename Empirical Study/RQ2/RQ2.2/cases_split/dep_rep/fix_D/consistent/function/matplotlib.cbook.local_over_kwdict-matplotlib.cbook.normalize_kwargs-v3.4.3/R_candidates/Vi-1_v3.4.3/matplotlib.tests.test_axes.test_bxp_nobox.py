@image_comparison(['bxp_nobox.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_nobox():
    _bxp_test_helper(bxp_kwargs=dict(showbox=False))
