@image_comparison(['bxp_customwhisker.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_customwhisker():
    _bxp_test_helper(bxp_kwargs=dict(
        whiskerprops=dict(linestyle='-', color='m', lw=3)))
