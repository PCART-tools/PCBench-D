@_wraps(scipy.linalg.lu, update_doc=False,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
@partial(jit, static_argnames=('permute_l', 'overwrite_a', 'check_finite'))
def lu(a: ArrayLike, permute_l: bool = False, overwrite_a: bool = False,
       check_finite: bool = True) -> Union[Tuple[Array, Array], Tuple[Array, Array, Array]]:
  del overwrite_a, check_finite  # unused
  return _lu(a, permute_l)
