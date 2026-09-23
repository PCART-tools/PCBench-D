@util.implements(np.matmul, module='numpy', lax_description=_PRECISION_DOC,
                 extra_params=_DOT_PREFERRED_ELEMENT_TYPE_DESCRIPTION)
@partial(jit, static_argnames=('precision', 'preferred_element_type'), inline=True)
def matmul(a: ArrayLike, b: ArrayLike, *,
           precision: PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None,
           ) -> Array:
  """Matrix Multiply."""
  util.check_arraylike("matmul", a, b)
  dtypes.check_user_dtype_supported(preferred_element_type, "matmul")
  a, b = asarray(a), asarray(b)
  for i, x in enumerate((a, b)):
    if ndim(x) < 1:
      msg = (f"matmul input operand {i} must have ndim at least 1, "
             f"but it has ndim {ndim(x)}")
      raise ValueError(msg)
  if preferred_element_type is None:
    preferred_element_type, output_weak_type = dtypes.result_type(a, b, return_weak_type_flag=True)
  else:
    output_weak_type = False

  a_is_mat, b_is_mat = (ndim(a) > 1), (ndim(b) > 1)
  a_batch_dims: tuple[int | None, ...] = shape(a)[:-2] if a_is_mat else ()
  b_batch_dims: tuple[int | None, ...] = shape(b)[:-2] if b_is_mat else ()
  num_batch_dims = max(len(a_batch_dims), len(b_batch_dims))
  a_batch_dims = (None,) * (num_batch_dims - len(a_batch_dims)) + a_batch_dims
  b_batch_dims = (None,) * (num_batch_dims - len(b_batch_dims)) + b_batch_dims

  # Dimensions to squeeze from the inputs.
  a_squeeze: list[int] = []
  b_squeeze: list[int] = []

  # Positions of batch dimensions in squeezed inputs.
  a_batch = []
  b_batch = []

  # Desired index in final output of each kind of dimension, in the order that
  # lax.dot_general will emit them.
  idx_batch: list[int] = []
  idx_a_other: list[int] = []  # other = non-batch, non-contracting.
  idx_b_other: list[int] = []
  for i, (ba, bb) in enumerate(zip(a_batch_dims, b_batch_dims)):
    if ba is None:
      idx_b_other.append(i)
    elif bb is None:
      idx_a_other.append(i)
    elif core.definitely_equal(ba, 1):
      idx_b_other.append(i)
      a_squeeze.append(len(idx_batch) + len(idx_a_other) + len(a_squeeze))
    elif core.definitely_equal(bb, 1):
      idx_a_other.append(i)
      b_squeeze.append(len(idx_batch) + len(idx_b_other) + len(b_squeeze))
    elif core.definitely_equal(ba, bb):
      a_batch.append(len(idx_batch) + len(idx_a_other))
      b_batch.append(len(idx_batch) + len(idx_b_other))
      idx_batch.append(i)
    else:
      raise ValueError("Incompatible shapes for matmul arguments: {} and {}"
                       .format(shape(a), shape(b)))

  if a_is_mat: idx_a_other.append(num_batch_dims)
  if b_is_mat: idx_b_other.append(num_batch_dims + a_is_mat)
  perm = np.argsort(np.concatenate([idx_batch, idx_a_other, idx_b_other]))

  a = lax.squeeze(a, tuple(a_squeeze))
  b = lax.squeeze(b, tuple(b_squeeze))
  out = lax.dot_general(
    a, b, (((ndim(a) - 1,), (ndim(b) - 1 - b_is_mat,)), (a_batch, b_batch)),
    precision=precision, preferred_element_type=preferred_element_type)
  result = lax.transpose(out, perm)
  return lax_internal._convert_element_type(result, preferred_element_type, output_weak_type)
