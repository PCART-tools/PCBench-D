@image_comparison(['bxp_customoutlier.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_customoutlier():
    _bxp_test_helper(bxp_kwargs=dict(
        flierprops=dict(linestyle='none', marker='d', mfc='g')))
