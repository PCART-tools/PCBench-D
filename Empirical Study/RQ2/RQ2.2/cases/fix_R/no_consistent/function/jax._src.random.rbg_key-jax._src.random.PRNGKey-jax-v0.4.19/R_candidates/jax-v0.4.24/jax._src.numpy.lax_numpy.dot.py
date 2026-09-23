@util.implements(np.dot, lax_description=_PRECISION_DOC,
                 extra_params=_DOT_PREFERRED_ELEMENT_TYPE_DESCRIPTION)
@partial(jit, static_argnames=('precision', 'preferred_element_type'), inline=True)
def dot(a: ArrayLike, b: ArrayLike, *,
        precision: PrecisionLike = None,
        preferred_element_type: DTypeLike | None = None) -> Array:
  util.check_arraylike("dot", a, b)
  dtypes.check_user_dtype_supported(preferred_element_type, "dot")
  a, b = asarray(a), asarray(b)
  if preferred_element_type is None:
    preferred_element_type, output_weak_type = dtypes.result_type(a, b, return_weak_type_flag=True)
  else:
    output_weak_type = False

  batch_dims = ((), ())
  a_ndim, b_ndim = ndim(a), ndim(b)
  if a_ndim == 0 or b_ndim == 0:
    # TODO(jakevdp): lower this case to dot_general as well?
    # Currently, doing so causes issues in remat tests due to #16805
    if preferred_element_type is not None:
      a = a.astype(preferred_element_type)
      b = b.astype(preferred_element_type)
    result = lax.mul(a, b)
  else:
    if b_ndim == 1:
      contract_dims = ((a_ndim - 1,), (0,))
    else:
      contract_dims = ((a_ndim - 1,), (b_ndim - 2,))
    result = lax.dot_general(a, b, dimension_numbers=(contract_dims, batch_dims),
                             precision=precision, preferred_element_type=preferred_element_type)
  return lax_internal._convert_element_type(result, preferred_element_type, output_weak_type)
