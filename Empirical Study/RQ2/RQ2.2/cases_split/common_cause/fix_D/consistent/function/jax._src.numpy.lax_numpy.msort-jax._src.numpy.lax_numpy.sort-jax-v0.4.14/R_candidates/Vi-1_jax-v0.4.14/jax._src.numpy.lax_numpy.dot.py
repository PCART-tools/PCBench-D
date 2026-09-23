@util._wraps(np.dot, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('precision',), inline=True)
def dot(a: ArrayLike, b: ArrayLike, *, precision: PrecisionLike = None) -> Array:  # pylint: disable=missing-docstring
  util.check_arraylike("dot", a, b)
  a, b = asarray(a), asarray(b)
  output_dtype, output_weak_type = dtypes.result_type(a, b, return_weak_type_flag=True)

  batch_dims = ((), ())
  a_ndim, b_ndim = ndim(a), ndim(b)
  if a_ndim == 0 or b_ndim == 0:
    # TODO(jakevdp): lower this case to dot_general as well?
    # Currently, doing so causes issues in remat tests due to #16805
    result = lax.mul(a.astype(output_dtype), b.astype(output_dtype))
  else:
    if b_ndim == 1:
      contract_dims = ((a_ndim - 1,), (0,))
    else:
      contract_dims = ((a_ndim - 1,), (b_ndim - 2,))
    result = lax.dot_general(a, b, dimension_numbers=(contract_dims, batch_dims),
                             precision=precision, preferred_element_type=output_dtype)
  return lax_internal._convert_element_type(result, output_dtype, output_weak_type)
