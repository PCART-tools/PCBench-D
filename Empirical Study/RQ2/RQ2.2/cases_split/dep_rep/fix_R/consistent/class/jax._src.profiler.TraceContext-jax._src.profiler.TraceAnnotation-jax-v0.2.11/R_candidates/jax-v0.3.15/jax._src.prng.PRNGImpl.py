class PRNGImpl(NamedTuple):
  """Specifies PRNG key shape and operations.

  A PRNG implementation is determined by a key type ``K`` and a
  collection of functions that operate on such keys. The key type
  ``K`` is an array type with element type uint32 and shape specified
  by ``key_shape``. The type signature of each operations is::

    seed :: int[] -> K
    fold_in :: K -> int[] -> K
    split[n] :: K -> K[n]
    random_bits[shape, bit_width] :: K -> uint<bit_width>[shape]

  A PRNG implementation is adapted to an array-like object of keys
  ``K`` by the ``PRNGKeyArray`` class, which should be created via the
  ``seed_with_impl`` function.
  """
  key_shape: core.Shape
  seed: Callable
  split: Callable
  random_bits: Callable
  fold_in: Callable

  def pprint(self):
    return (pp.text(f"{self.__class__.__name__}:") +
            pp.nest(2, pp.group(pp.brk() + pp.join(pp.brk(), [
              pp.text(f"{k} = {v}") for k, v in self._asdict().items()
            ]))))
