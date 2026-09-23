@image_comparison(['bxp_nocaps.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_nocaps():
    _bxp_test_helper(bxp_kwargs=dict(showcaps=False))
