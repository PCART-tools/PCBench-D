def check_type(
    ctx_factory: Callable[[], Tuple[JaxprPpContext, JaxprPpSettings]],
    env: Set[Var],
    ty: AbstractValue,
  ) -> None:
  if isinstance(ty, DShapedArray):
    # Check all elements in the shape tuple are well-typed.
    for d in ty.shape:
      if (isinstance(d, int) or
          isinstance(d, DArray) and not d.shape and type(d.dtype) == bint):
        continue
      elif isinstance(d, Var):
        if d not in env:
          ctx, _ = ctx_factory()
          raise JaxprTypeError(f"unbound axis size: '{pp_var(d, ctx)}'")
        if not isinstance(d.aval, (ShapedArray, DShapedArray)):
          raise JaxprTypeError(f"axis size with unexpected type annotation: "
                               f"{d.aval} of type {type(d.aval)}")
        if isinstance(d.aval, ShapedArray):
          shape, dtype = d.aval.shape, d.aval.dtype
          if shape: raise JaxprTypeError(f"axis size nonscalar: {d.aval}")
          if not dtypes.issubdtype(dtype, np.integer):
            raise JaxprTypeError(f"axis size with non-integer dtype: {d.aval}")
        else:
          assert isinstance(d.aval, DShapedArray)
          shape, dtype = d.aval.shape, d.aval.dtype
          if shape: raise JaxprTypeError(f"axis size nonscalar: {d.aval}")
          if type(dtype) is not bint:
            raise JaxprTypeError(
                f"DArray axis size with non-bint dtype: {d.aval}")
      else:
        raise JaxprTypeError(f"unexpected type in shape: {type(d)}")
  else:
    return  # Except in above case(s), all syntactic forms are valid
