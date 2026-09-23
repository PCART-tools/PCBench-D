def compute(*args, **kwargs):
    """deprecated, please use ``dask.compute``"""
    warnings.warn("`dask.delayed.compute` is deprecated, please use "
                  "`dask.compute` instead")
    return base.compute(*args, **kwargs)
