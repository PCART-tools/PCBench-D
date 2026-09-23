@_wraps(
    np.linalg.slogdet,
    extra_params=textwrap.dedent("""
      method: string, optional
        One of ``lu`` or ``qr``, specifying whether the determinant should be
        computed using an LU decomposition or a QR decomposition. Defaults to
        LU decomposition if ``None``.
    """))
@partial(jit, static_argnames=('method',))
def slogdet(a: ArrayLike, *, method: Optional[str] = None) -> Tuple[Array, Array]:
  check_arraylike("jnp.linalg.slogdet", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  a_shape = jnp.shape(a)
  if len(a_shape) < 2 or a_shape[-1] != a_shape[-2]:
    msg = "Argument to slogdet() must have shape [..., n, n], got {}"
    raise ValueError(msg.format(a_shape))

  if method is None or method == "lu":
    return _slogdet_lu(a)
  elif method == "qr":
    return _slogdet_qr(a)
  else:
    raise ValueError(f"Unknown slogdet method '{method}'. Supported methods "
                     "are 'lu' (`None`), and 'qr'.")
