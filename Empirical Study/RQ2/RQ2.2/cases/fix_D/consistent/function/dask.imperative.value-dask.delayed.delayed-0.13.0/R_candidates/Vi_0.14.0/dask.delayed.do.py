def do(*args, **kwargs):
    """deprecated, please use ``dask.delayed.delayed``"""
    warnings.warn("`dask.delayed.do` is deprecated, please use "
                  "`dask.delayed.delayed` instead")
    return delayed(*args, **kwargs)
