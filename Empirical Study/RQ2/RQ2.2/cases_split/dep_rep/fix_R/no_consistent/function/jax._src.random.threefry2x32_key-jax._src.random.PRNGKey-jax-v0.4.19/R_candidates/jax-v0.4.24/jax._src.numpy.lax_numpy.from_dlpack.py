@util.implements(getattr(np, "from_dlpack", None), lax_description="""
.. note::

   While JAX arrays are always immutable, dlpack buffers cannot be marked as
   immutable, and it is possible for processes external to JAX to mutate them
   in-place. If a jax Array is constructed from a dlpack buffer and the buffer
   is later modified in-place, it may lead to undefined behavior when using
   the associated JAX array.
""")
def from_dlpack(x: Any) -> Array:
  from jax.dlpack import from_dlpack  # pylint: disable=g-import-not-at-top
  return from_dlpack(x.__dlpack__())
