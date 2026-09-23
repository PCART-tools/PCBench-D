@image_comparison(['bxp_percentilewhis.png'],
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_percentilewhis():
    _bxp_test_helper(stats_kwargs=dict(whis=[5, 95]))
