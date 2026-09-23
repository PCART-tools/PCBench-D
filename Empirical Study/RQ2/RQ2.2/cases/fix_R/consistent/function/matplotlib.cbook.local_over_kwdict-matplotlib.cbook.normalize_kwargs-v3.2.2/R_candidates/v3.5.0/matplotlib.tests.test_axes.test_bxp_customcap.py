@image_comparison(['bxp_customcap.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_customcap():
    _bxp_test_helper(bxp_kwargs=dict(
        capprops=dict(linestyle='--', color='g', lw=3)))
