def coerce_boundary(ndim, boundary):
    if boundary is None:
        boundary = 'reflect'
    if not isinstance(boundary, (tuple, dict)):
        boundary = (boundary,) * ndim
    if isinstance(boundary, tuple):
        boundary = dict(zip(range(ndim), boundary))
    return boundary
