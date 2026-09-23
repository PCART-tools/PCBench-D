@image_comparison(['bxp_custombox.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_custombox():
    _bxp_test_helper(bxp_kwargs=dict(
        boxprops=dict(linestyle='--', color='b', lw=3)))
