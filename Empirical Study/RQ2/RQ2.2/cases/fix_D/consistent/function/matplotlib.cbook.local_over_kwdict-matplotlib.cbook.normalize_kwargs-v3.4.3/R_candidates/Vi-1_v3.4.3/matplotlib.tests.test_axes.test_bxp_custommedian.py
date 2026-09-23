@image_comparison(['bxp_custommedian.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_custommedian():
    _bxp_test_helper(bxp_kwargs=dict(
        medianprops=dict(linestyle='--', color='b', lw=3)))
