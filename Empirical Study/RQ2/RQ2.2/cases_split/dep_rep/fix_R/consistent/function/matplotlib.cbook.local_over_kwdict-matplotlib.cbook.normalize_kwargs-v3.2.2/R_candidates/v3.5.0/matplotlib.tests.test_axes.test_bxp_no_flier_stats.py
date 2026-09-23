@image_comparison(['bxp_no_flier_stats.png'],
                  remove_text=True,
                  savefig_kwarg={'dpi': 40},
                  style='default')
def test_bxp_no_flier_stats():
    def transform(stats):
        for s in stats:
            s.pop('fliers', None)
        return stats

    _bxp_test_helper(transform_stats=transform,
                     bxp_kwargs=dict(showfliers=False))
