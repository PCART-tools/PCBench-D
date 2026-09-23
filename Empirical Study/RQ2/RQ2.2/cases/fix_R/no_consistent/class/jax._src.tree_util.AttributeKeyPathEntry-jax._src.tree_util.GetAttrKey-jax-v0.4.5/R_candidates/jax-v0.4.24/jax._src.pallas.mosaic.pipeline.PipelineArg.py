@tree_util.register_pytree_node_class
@dataclasses.dataclass(frozen=True)
class PipelineArg(Generic[T]):
  """Wrapper for pipeline arguments that exist for inputs, outputs, and accums."""
  input: T
  out: T
  in_out: T

  @property
  def input_and_in_out(self) -> T:
    return cast(Any, self.input) + cast(Any, self.in_out)

  def tree_flatten(self):
    return ((self.input, self.out, self.in_out), None)

  @classmethod
  def tree_unflatten(cls, _, children):
    return cls(*children)
