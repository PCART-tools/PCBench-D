def _resample(obj, rule, how, **kwargs):
    resampler = Resampler(obj, rule, **kwargs)
    if how is not None:
        w = FutureWarning(("how in .resample() is deprecated "
                           "the new syntax is .resample(...)"
                           ".{0}()").format(how))
        warnings.warn(w)
        return getattr(resampler, how)()
    return resampler
