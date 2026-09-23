    def _resample(obj, rule, how, **kwargs):
        how = how or 'mean'
        return getattr(Resampler(obj, rule, **kwargs), how)()
