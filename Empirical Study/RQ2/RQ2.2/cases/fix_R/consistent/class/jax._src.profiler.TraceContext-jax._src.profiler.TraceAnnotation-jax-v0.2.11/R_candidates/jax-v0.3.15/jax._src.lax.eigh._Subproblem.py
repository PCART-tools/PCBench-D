class _Subproblem(NamedTuple):
  """Describes a subproblem of _eigh_work.

  Each subproblem is a `size` x `size` Hermitian matrix, starting at `offset`
  in the workspace.
  """
  # The row offset of the block in the matrix of blocks.
  offset: jnp.ndarray

  # The size of the block.
  size: jnp.ndarray
