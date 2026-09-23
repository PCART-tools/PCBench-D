@image_comparison(['bxp_withnotch.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_shownotches():
    _bxp_test_helper(bxp_kwargs=dict(shownotches=True))
