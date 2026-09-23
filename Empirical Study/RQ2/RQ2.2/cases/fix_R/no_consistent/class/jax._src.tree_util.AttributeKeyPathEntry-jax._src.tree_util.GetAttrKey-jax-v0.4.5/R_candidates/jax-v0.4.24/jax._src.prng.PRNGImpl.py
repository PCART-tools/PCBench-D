class PRNGImpl(NamedTuple):
  """Specifies PRNG key shape and operations.

  A PRNG implementation is determined by a key type ``K`` and a
  collection of functions that operate on such keys. The key type
  ``K`` is an array type with element type uint32 and shape specified
  by ``key_shape``. The type signature of each operations is::

    seed :: int[] -> K
    fold_in :: K -> int[] -> K
    split[shape] :: K -> K[*shape]
    random_bits[shape, bit_width] :: K -> uint<bit_width>[*shape]

  A PRNG implementation is adapted to an array-like object of keys
  ``K`` by the ``PRNGKeyArray`` class, which should be created via the
  ``random_seed`` function.
  """
  key_shape: Shape
  seed: Callable
  split: Callable
  random_bits: Callable
  fold_in: Callable
  name: str = '<unnamed>'
  tag: str = '?'

  def __hash__(self) -> int:
    return hash(self.tag)

  def __str__(self) -> str:
    return self.tag

  def pprint(self):
    ty = self.__class__.__name__
    return (pp.text(f"{ty} [{self.tag}] {{{self.name}}}:") +
            pp.nest(2, pp.group(pp.brk() + pp.join(pp.brk(), [
              pp.text(f"{k} = {v}") for k, v in self._asdict().items()
            ]))))
