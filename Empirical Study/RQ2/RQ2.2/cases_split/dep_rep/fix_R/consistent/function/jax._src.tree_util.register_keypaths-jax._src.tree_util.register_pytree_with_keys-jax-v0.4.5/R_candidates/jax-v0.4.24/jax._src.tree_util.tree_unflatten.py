def tree_unflatten(treedef: PyTreeDef, leaves: Iterable[Leaf]) -> Any:
  """Reconstructs a pytree from the treedef and the leaves.

  The inverse of :func:`tree_flatten`.

  Args:
    treedef: the treedef to reconstruct
    leaves: the iterable of leaves to use for reconstruction. The iterable must
      match the leaves of the treedef.

  Returns:
    The reconstructed pytree, containing the ``leaves`` placed in the structure
    described by ``treedef``.
  """
  return treedef.unflatten(leaves)
