@image_comparison(['bxp_custompositions.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_custompositions():
    _bxp_test_helper(bxp_kwargs=dict(positions=[1, 5, 6, 7]))
