@image_comparison(['bxp_withmean_line.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_showmeanasline():
    _bxp_test_helper(bxp_kwargs=dict(showmeans=True, meanline=True))
