def handle_out(out, result):
    """ Handle out parameters

    If out is a dask.array then this overwrites the contents of that array with
    the result
    """
    if isinstance(out, tuple):
        if len(out) == 1:
            out = out[0]
        elif len(out) > 1:
            raise NotImplementedError("The out parameter is not fully supported")
        else:
            out = None
    if isinstance(out, Array):
        if out.shape != result.shape:
            raise ValueError(
                "Mismatched shapes between result and out parameter. "
                "out=%s, result=%s" % (str(out.shape), str(result.shape)))
        out._chunks = result.chunks
        out.dask = result.dask
        out.dtype = result.dtype
        out.name = result.name
    elif out is not None:
        msg = ("The out parameter is not fully supported."
               " Received type %s, expected Dask Array" % type(out).__name__)
        raise NotImplementedError(msg)
    else:
        return result
