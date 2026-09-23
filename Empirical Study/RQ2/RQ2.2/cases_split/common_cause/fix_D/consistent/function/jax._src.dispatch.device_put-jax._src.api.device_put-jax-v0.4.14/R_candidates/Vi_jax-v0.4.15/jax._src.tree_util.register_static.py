def register_static(cls: Type[H]) -> Type[H]:
  """Registers `cls` as a pytree with no leaves.

  Instances are treated as static by `jax.jit`, `jax.pmap`, etc. This can be an
  alternative to labeling inputs as static using `jax.jit`'s `static_argnums`
  and `static_argnames` kwargs, `jax.pmap`'s `static_broadcasted_argnums`, etc.

  `cls` must be hashable, as defined in
  https://docs.python.org/3/glossary.html#term-hashable.

  `register_static` can be applied to subclasses of builtin hashable classes
  such as `str`, like this:
  ```
  @tree_util.register_static
  class StaticStr(str):
    pass
  ```
  """
  flatten = lambda obj: ((), obj)
  unflatten = lambda obj, empty_iter_children: obj
  register_pytree_with_keys(cls, flatten, unflatten)
  return cls
