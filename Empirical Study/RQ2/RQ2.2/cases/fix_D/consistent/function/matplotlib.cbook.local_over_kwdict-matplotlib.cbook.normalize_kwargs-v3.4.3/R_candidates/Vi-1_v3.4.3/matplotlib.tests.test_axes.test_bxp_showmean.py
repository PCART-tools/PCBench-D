@image_comparison(['bxp_withmean_point.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_showmean():
    _bxp_test_helper(bxp_kwargs=dict(showmeans=True, meanline=False))
