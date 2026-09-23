def _convert_element_type(operand: ArrayLike, new_dtype: Optional[DTypeLike] = None,
                          weak_type: bool = False):
  if hasattr(operand, '__jax_array__'):
    operand = operand.__jax_array__()  # type: ignore

  if (dtypes.issubdtype(new_dtype, dtypes.extended) or
      dtypes.issubdtype(getattr(operand, 'dtype', None), dtypes.extended)):
    return convert_element_type_p.bind(operand, new_dtype=new_dtype,
                                       weak_type=bool(weak_type))

  # Don't canonicalize old_dtype because x64 context might cause
  # un-canonicalized operands to be passed in.
  old_dtype = dtypes.dtype(operand, canonicalize=False)
  old_weak_type = dtypes.is_weakly_typed(operand)
  if new_dtype is None:
    new_dtype = old_dtype
  else:
    new_dtype = np.dtype(new_dtype)
  new_dtype = dtypes.dtype(new_dtype, canonicalize=True)

  if (dtypes.issubdtype(old_dtype, np.complexfloating) and
      not dtypes.issubdtype(new_dtype, np.complexfloating)):
    msg = "Casting complex values to real discards the imaginary part"
    warnings.warn(msg, np.ComplexWarning, stacklevel=2)

  # Python has big integers, but convert_element_type(2 ** 100, np.float32) need
  # not be an error since the target dtype fits the value. Handle this case by
  # converting to a NumPy array before calling bind. Without this step, we'd
  # first canonicalize the input to a value of dtype int32 or int64, leading to
  # an overflow error.
  if type(operand) is int:
    operand = np.asarray(operand).astype(new_dtype)
    old_weak_type = False

  if ((old_dtype, old_weak_type) == (new_dtype, weak_type) and
      isinstance(operand, Array) and
      not (isinstance(operand, core.Tracer) and
           isinstance(core.get_aval(operand), core.ConcreteArray))):
    return type_cast(Array, operand)
  else:
    return convert_element_type_p.bind(operand, new_dtype=new_dtype,
                                       weak_type=bool(weak_type))
