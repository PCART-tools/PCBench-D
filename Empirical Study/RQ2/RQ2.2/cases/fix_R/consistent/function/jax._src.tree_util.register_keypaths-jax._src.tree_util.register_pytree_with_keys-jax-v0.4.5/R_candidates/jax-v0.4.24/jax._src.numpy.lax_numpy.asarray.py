@util.implements(np.asarray, lax_description=_ARRAY_DOC)
def asarray(a: Any, dtype: DTypeLike | None = None, order: str | None = None,
            *, copy: bool | None = None) -> Array:
  # For copy=False, the array API specifies that we raise a ValueError if the input supports
  # the buffer protocol but a copy is required. Since array() supports the buffer protocol
  # via numpy, this is only the case when the default device is not 'cpu'
  if (copy is False and not isinstance(a, Array)
      and jax.default_backend() != 'cpu'
      and _supports_buffer_protocol(a)):
    raise ValueError(f"jnp.asarray: cannot convert object of type {type(a)} to JAX Array "
                     f"on backend={jax.default_backend()!r} with copy=False. "
                      "Consider using copy=None or copy=True instead.")
  dtypes.check_user_dtype_supported(dtype, "asarray")
  if dtype is not None:
    dtype = dtypes.canonicalize_dtype(dtype, allow_extended_dtype=True)  # type: ignore[assignment]
  return array(a, dtype=dtype, copy=bool(copy), order=order)  # type: ignore
