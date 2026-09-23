@export
@typing.runtime_checkable
class Initializer(Protocol):
  @staticmethod
  def __call__(key: KeyArray,
               shape: core.Shape,
               dtype: DTypeLikeInexact = jnp.float_) -> Array:
    raise NotImplementedError
