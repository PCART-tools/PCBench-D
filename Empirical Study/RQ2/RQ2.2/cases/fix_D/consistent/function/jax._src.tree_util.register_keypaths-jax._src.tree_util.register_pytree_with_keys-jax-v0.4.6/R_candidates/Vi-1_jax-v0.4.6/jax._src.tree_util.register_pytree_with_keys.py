def register_pytree_with_keys(
    nodetype: Type[T],
    flatten_with_keys: Callable[[T], Tuple[Iterable[Tuple[KeyPath, _Children]], _AuxData]],
    unflatten_func: Callable[[_AuxData, _Children], T]):
  """Extends the set of types that are considered internal nodes in pytrees.

  This is a more powerful alternative to ``register_pytree_node`` that allows
  you to access each pytree leaf's key path when flattening and tree-mapping.

  Args:
    nodetype: a Python type to treat as an internal pytree node.
    flatten_func: a function to be used during flattening, taking a value of
      type ``nodetype`` and returning a pair, with (1) an iterable for tuples of
      each key path and its child, and (2) some hashable auxiliary data to be
      stored in the treedef and to be passed to the ``unflatten_func``.
    unflatten_func: a function taking two arguments: the auxiliary data that was
      returned by ``flatten_func`` and stored in the treedef, and the
      unflattened children. The function should return an instance of
      ``nodetype``.
  """
  def flatten_func(tree):
    key_children, treedef = flatten_with_keys(tree)
    return [c for _, c in key_children], treedef
  register_pytree_node(nodetype, flatten_func, unflatten_func)
  _registry_with_keypaths[nodetype] = _RegistryWithKeypathsEntry(
      flatten_with_keys, unflatten_func
  )
