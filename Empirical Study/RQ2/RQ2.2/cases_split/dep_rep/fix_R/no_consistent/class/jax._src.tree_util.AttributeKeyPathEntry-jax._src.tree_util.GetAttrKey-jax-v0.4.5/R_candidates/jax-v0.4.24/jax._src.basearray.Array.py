class Array(abc.ABC):
  """Array base class for JAX

  ``jax.Array`` is the public interface for instance checks and type annotation
  of JAX arrays and tracers. Its main applications are in instance checks and
  type annotations; for example::

    x = jnp.arange(5)
    isinstance(x, jax.Array)  # returns True both inside and outside traced functions.

    def f(x: Array) -> Array:  # type annotations are valid for traced and non-traced types.
      return x

  ``jax.Array`` should not be used directly for creation of arrays; instead you
  should use array creation routines offered in :mod:`jax.numpy`, such as
  :func:`jax.numpy.array`, :func:`jax.numpy.zeros`, :func:`jax.numpy.ones`,
  :func:`jax.numpy.full`, :func:`jax.numpy.arange`, etc.
  """
  # Note: abstract methods for this class are defined dynamically in
  # lax_numpy.py
  # For the sake of static type analysis, these definitions are mirrored in the
  # associated basearray.pyi file.

  __slots__ = ['__weakref__']

  @property
  @abc.abstractmethod
  def dtype(self) -> np.dtype:
    """The data type (:class:`numpy.dtype`) of the array."""

  @property
  @abc.abstractmethod
  def ndim(self) -> int:
    """The number of dimensions in the array."""

  @property
  @abc.abstractmethod
  def size(self) -> int:
    """The total number of elements in the array."""

  @property
  @abc.abstractmethod
  def shape(self) -> tuple[int, ...]:
    """The shape of the array."""

  # Documentation for sharding-related methods and properties defined on ArrayImpl:
  @abc.abstractmethod
  def addressable_data(self, index: int) -> Array:
    """Return an array of the addressable data at a particular index."""

  @property
  @abc.abstractmethod
  def addressable_shards(self) -> Sequence[Shard]:
    """List of addressable shards."""

  @property
  @abc.abstractmethod
  def global_shards(self) -> Sequence[Shard]:
    """List of global shards."""

  @property
  @abc.abstractmethod
  def is_fully_addressable(self) -> bool:
    """Is this Array fully addressable?

    A jax.Array is fully addressable if the current process can address all of
    the devices named in the :class:`Sharding`. ``is_fully_addressable`` is
    equivalent to "is_local" in multi-process JAX.

    Note that fully replicated is not equal to fully addressable i.e.
    a jax.Array which is fully replicated can span across multiple hosts and is
    not fully addressable.
    """

  @property
  @abc.abstractmethod
  def is_fully_replicated(self) -> bool:
    """Is this Array fully replicated?"""

  @property
  @abc.abstractmethod
  def sharding(self) -> Sharding:
    """The sharding for the array."""
