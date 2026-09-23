def register_pytree_node(nodetype: type[T],
                         flatten_func: Callable[[T], tuple[_Children, _AuxData]],
                         unflatten_func: Callable[[_AuxData, _Children], T]):
  """Extends the set of types that are considered internal nodes in pytrees.

  See :ref:`example usage <pytrees>`.

  Args:
    nodetype: a Python type to treat as an internal pytree node.
    flatten_func: a function to be used during flattening, taking a value of
      type ``nodetype`` and returning a pair, with (1) an iterable for the
      children to be flattened recursively, and (2) some hashable auxiliary data
      to be stored in the treedef and to be passed to the ``unflatten_func``.
    unflatten_func: a function taking two arguments: the auxiliary data that was
      returned by ``flatten_func`` and stored in the treedef, and the
      unflattened children. The function should return an instance of
      ``nodetype``.
  """
  default_registry.register_node(nodetype, flatten_func, unflatten_func)
  dispatch_registry.register_node(nodetype, flatten_func, unflatten_func)
  _registry[nodetype] = _RegistryEntry(flatten_func, unflatten_func)
