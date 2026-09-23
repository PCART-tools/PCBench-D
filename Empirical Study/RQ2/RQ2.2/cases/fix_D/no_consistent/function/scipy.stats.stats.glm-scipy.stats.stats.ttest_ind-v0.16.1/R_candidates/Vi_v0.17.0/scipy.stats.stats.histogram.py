@np.deprecate(message=("scipy.stats.histogram is deprecated in scipy 0.17.0; "
                       "use np.histogram instead"))
def histogram(a, numbins=10, defaultlimits=None, weights=None, printextras=False):
    # _histogram is used in relfreq/cumfreq, so need to keep it
    res = _histogram(a, numbins=numbins, defaultlimits=defaultlimits,
                     weights=weights, printextras=printextras)
    return res
