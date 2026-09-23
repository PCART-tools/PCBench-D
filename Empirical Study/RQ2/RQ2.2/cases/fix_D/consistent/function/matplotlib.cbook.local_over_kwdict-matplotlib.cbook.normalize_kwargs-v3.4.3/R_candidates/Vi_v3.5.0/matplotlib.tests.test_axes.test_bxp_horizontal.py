@image_comparison(['bxp_horizontal.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default',
                  tol=0.1)
def test_bxp_horizontal():
    _bxp_test_helper(bxp_kwargs=dict(vert=False))
