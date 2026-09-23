def to_dlpack(x: Array, take_ownership: bool = False,
              stream: int | None = None):
  """Returns a DLPack tensor that encapsulates a :class:`~jax.Array` ``x``.

  Takes ownership of the contents of ``x``; leaves ``x`` in an invalid/deleted
  state.

  Args:
    x: a :class:`~jax.Array`, on either CPU or GPU.
    take_ownership: If ``True``, JAX hands ownership of the buffer to DLPack,
      and the consumer is free to mutate the buffer; the JAX buffer acts as if
      it were deleted. If ``False``, JAX retains ownership of the buffer; it is
      undefined behavior if the DLPack consumer writes to a buffer that JAX
      owns.
    stream: optional platform-dependent stream to wait on until the buffer is
      ready. This corresponds to the `stream` argument to ``__dlpack__``
      documented in https://dmlc.github.io/dlpack/latest/python_spec.html.
  """
  if not isinstance(x, array.ArrayImpl):
    raise TypeError("Argument to to_dlpack must be a jax.Array, "
                    f"got {type(x)}")
  assert len(x.devices()) == 1
  if xla_extension_version >= 186:
    return xla_client._xla.buffer_to_dlpack_managed_tensor(
        x.addressable_data(0), take_ownership=take_ownership, stream=stream
    )  # type: ignore
  else:
    if stream is not None:
      raise ValueError(
          "passing `stream` argument to to_dlpack requires jaxlib >= 0.4.15")
    return xla_client._xla.buffer_to_dlpack_managed_tensor(
        x.addressable_data(0), take_ownership=take_ownership)  # type: ignore
