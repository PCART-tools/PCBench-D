@_wraps(scipy.ndimage.map_coordinates, lax_description=textwrap.dedent("""\
    Only nearest neighbor (``order=0``), linear interpolation (``order=1``) and
    modes ``'constant'``, ``'nearest'``, ``'wrap'`` ``'mirror'`` and ``'reflect'`` are currently supported.
    Note that interpolation near boundaries differs from the scipy function,
    because we fixed an outstanding bug (https://github.com/scipy/scipy/issues/2640);
    this function interprets the ``mode`` argument as documented by SciPy, but
    not as implemented by SciPy.
    """))
def map_coordinates(
    input, coordinates, order, mode='constant', cval=0.0,
):
  return _map_coordinates(input, coordinates, order, mode, cval)
