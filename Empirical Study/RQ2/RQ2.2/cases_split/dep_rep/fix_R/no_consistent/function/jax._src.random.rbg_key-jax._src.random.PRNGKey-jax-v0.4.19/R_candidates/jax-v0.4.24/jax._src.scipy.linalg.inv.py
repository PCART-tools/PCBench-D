@implements(scipy.linalg.inv,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
def inv(a: ArrayLike, overwrite_a: bool = False, check_finite: bool = True) -> Array:
  del overwrite_a, check_finite  # unused
  return jnp.linalg.inv(a)
