    def _resample_apply(s, rule, how, resample_kwargs):
        return s.resample(rule, how=how, **resample_kwargs)
