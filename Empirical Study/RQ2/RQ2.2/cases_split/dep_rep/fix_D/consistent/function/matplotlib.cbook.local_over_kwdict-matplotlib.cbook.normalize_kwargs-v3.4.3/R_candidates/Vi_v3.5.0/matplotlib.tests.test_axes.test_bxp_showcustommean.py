@image_comparison(['bxp_withmean_custompoint.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_showcustommean():
    _bxp_test_helper(bxp_kwargs=dict(
        showmeans=True,
        meanprops=dict(linestyle='none', marker='d', mfc='green'),
    ))
