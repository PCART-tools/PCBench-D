@util.implements(np.take, skip_params=['out'],
        lax_description="""
By default, JAX assumes that all indices are in-bounds. Alternative out-of-bound
index semantics can be specified via the ``mode`` parameter (see below).
""",
        extra_params="""
mode : string, default="fill"
    Out-of-bounds indexing mode. The default mode="fill" returns invalid values
    (e.g. NaN) for out-of bounds indices (see also ``fill_value`` below).
    For more discussion of mode options, see :attr:`jax.numpy.ndarray.at`.
fill_value : optional
    The fill value to return for out-of-bounds slices when mode is 'fill'. Ignored
    otherwise. Defaults to NaN for inexact types, the largest negative value for
    signed types, the largest positive value for unsigned types, and True for booleans.
unique_indices : bool, default=False
    If True, the implementation will assume that the indices are unique,
    which can result in more efficient execution on some backends.
indices_are_sorted : bool, default=False
    If True, the implementation will assume that the indices are sorted in
    ascending order, which can lead to more efficient execution on some backends.
""")
def take(
    a: ArrayLike,
    indices: ArrayLike,
    axis: int | None = None,
    out: None = None,
    mode: str | None = None,
    unique_indices: bool = False,
    indices_are_sorted: bool = False,
    fill_value: ArrayLike | None = None,
) -> Array:
  return _take(a, indices, None if axis is None else operator.index(axis), out,
               mode, unique_indices=unique_indices, indices_are_sorted=indices_are_sorted,
               fill_value=fill_value)
