def to_dlpack(x: Array, take_ownership: bool = False,
              stream: int | Any | None = None):
  """Returns a DLPack tensor that encapsulates a :class:`~jax.Array` ``x``.

  Args:
    x: a :class:`~jax.Array`, on either CPU or GPU.
    take_ownership: Deprecated. It is a no-op to set take_ownership. Will be
      deleted in 01/2024.
    stream: optional platform-dependent stream to wait on until the buffer is
      ready. This corresponds to the `stream` argument to ``__dlpack__``
      documented in https://dmlc.github.io/dlpack/latest/python_spec.html.

  Returns:
    A dlpack PyCapsule object.

  Note:
    While JAX arrays are always immutable, dlpack buffers cannot be marked as
    immutable, and it is possible for processes external to JAX to mutate them
    in-place. If a dlpack buffer derived from a JAX array is mutated, it may
    lead to undefined behavior when using the associated JAX array.
  """
  if not isinstance(x, array.ArrayImpl):
    raise TypeError("Argument to to_dlpack must be a jax.Array, "
                    f"got {type(x)}")
  assert len(x.devices()) == 1
  if take_ownership:
    warnings.warn(
        "take_ownership in to_dlpack is deprecated and it is a no-op."
    )
  return xla_client._xla.buffer_to_dlpack_managed_tensor(
      x.addressable_data(0), stream=stream
  )  # type: ignore
