@wraps(np.ma.masked_array)
def masked_array(data, mask=np.ma.nomask, fill_value=None,
                 **kwargs):
    data = asanyarray(data)
    inds = tuple(range(data.ndim))
    arginds = [inds, data, inds]

    if getattr(fill_value, 'shape', ()):
        raise ValueError("non-scalar fill_value not supported")
    kwargs['fill_value'] = fill_value

    if mask is not np.ma.nomask:
        mask = asanyarray(mask)
        if mask.size == 1:
            mask = mask.reshape((1,) * data.ndim)
        elif data.shape != mask.shape:
            raise np.ma.MaskError("Mask and data not compatible: data shape "
                                  "is %s, and mask shape is "
                                  "%s." % (repr(data.shape), repr(mask.shape)))
        arginds.extend([mask, inds])

    if 'dtype' in kwargs:
        kwargs['masked_dtype'] = kwargs['dtype']
    else:
        kwargs['dtype'] = data.dtype

    return atop(_masked_array, *arginds, **kwargs)
