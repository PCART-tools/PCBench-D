def to_dlpack(x: Array, take_ownership: bool = False):
  """Returns a DLPack tensor that encapsulates a ``DeviceArray`` `x`.

  Takes ownership of the contents of ``x``; leaves `x` in an invalid/deleted
  state.

  Args:
    x: a ``DeviceArray``, on either CPU or GPU.
    take_ownership: If ``True``, JAX hands ownership of the buffer to DLPack,
      and the consumer is free to mutate the buffer; the JAX buffer acts as if
      it were deleted. If ``False``, JAX retains ownership of the buffer; it is
      undefined behavior if the DLPack consumer writes to a buffer that JAX
      owns.
  """
  if not isinstance(x, array.ArrayImpl):
    raise TypeError("Argument to to_dlpack must be a jax.Array, "
                    f"got {type(x)}")
  assert len(x.devices()) == 1
  return xla_client._xla.buffer_to_dlpack_managed_tensor(
      x.addressable_data(0), take_ownership=take_ownership)  # type: ignore
