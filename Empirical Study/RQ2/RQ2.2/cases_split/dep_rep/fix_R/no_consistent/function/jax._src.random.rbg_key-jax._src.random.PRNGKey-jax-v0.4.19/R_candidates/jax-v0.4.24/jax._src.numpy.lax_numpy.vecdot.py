@util.implements(getattr(np, "vecdot", None), lax_description=_PRECISION_DOC,
                 extra_params=_DOT_PREFERRED_ELEMENT_TYPE_DESCRIPTION)
def vecdot(x1: ArrayLike, x2: ArrayLike, /, *, axis: int = -1,
           precision: PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None) -> Array:
  util.check_arraylike("jnp.vecdot", x1, x2)
  x1_arr, x2_arr = asarray(x1), asarray(x2)
  if x1_arr.shape[axis] != x2_arr.shape[axis]:
    raise ValueError(f"axes must match; got shapes {x1_arr.shape} and {x2_arr.shape} with {axis=}")
  x1_arr = jax.numpy.moveaxis(x1_arr, axis, -1)
  x2_arr = jax.numpy.moveaxis(x2_arr, axis, -1)
  return vectorize(partial(vdot, precision=precision, preferred_element_type=preferred_element_type),
                   signature="(n),(n)->()")(x1_arr, x2_arr)
