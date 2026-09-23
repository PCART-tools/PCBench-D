@image_comparison(['bxp_rangewhis.png'],
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_rangewhis():
    _bxp_test_helper(stats_kwargs=dict(whis=[0, 100]))
