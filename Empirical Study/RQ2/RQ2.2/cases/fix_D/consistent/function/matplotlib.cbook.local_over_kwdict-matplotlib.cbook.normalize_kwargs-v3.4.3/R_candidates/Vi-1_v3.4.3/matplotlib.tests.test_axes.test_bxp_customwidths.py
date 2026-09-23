@image_comparison(['bxp_customwidths.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_customwidths():
    _bxp_test_helper(bxp_kwargs=dict(widths=[0.10, 0.25, 0.65, 0.85]))
