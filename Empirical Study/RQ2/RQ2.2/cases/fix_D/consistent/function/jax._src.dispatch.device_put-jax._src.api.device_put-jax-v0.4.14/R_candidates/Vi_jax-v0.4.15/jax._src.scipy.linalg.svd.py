@_wraps(scipy.linalg.svd,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite', 'lapack_driver'))
def svd(a: ArrayLike, full_matrices: bool = True, compute_uv: bool = True,
        overwrite_a: bool = False, check_finite: bool = True,
        lapack_driver: str = 'gesdd') -> Union[Array, tuple[Array, Array, Array]]:
  del overwrite_a, check_finite, lapack_driver  # unused
  return _svd(a, full_matrices=full_matrices, compute_uv=compute_uv)
