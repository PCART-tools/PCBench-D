def _scatter_batching_rule(scatter_op, batched_args, batch_dims, *,
                           update_jaxpr, update_consts, dimension_numbers,
                           indices_are_sorted, unique_indices, mode):
  operand, indices, updates = batched_args
  operand_bdim, indices_bdim, updates_bdim = batch_dims
  del update_jaxpr, update_consts  # Unused.

  # move the operand batch dim to the front if it is not None, otherwise create
  # it at the front (so that we can scatter into it)
  size = next(x.shape[ax] for x, ax in zip(batched_args, batch_dims)
              if ax is not None)
  operand = batching.bdim_at_front(operand, operand_bdim, size)
  operand_bdim = 0

  updates = batching.bdim_at_front(updates, updates_bdim, size)

  if indices_bdim is None:
    inserted_window_dims = tuple(np.add(1, dimension_numbers.inserted_window_dims))
    update_window_dims = (0,) + tuple(np.add(1, dimension_numbers.update_window_dims))
    scatter_dims_to_operand_dims = tuple(np.add(1, dimension_numbers.scatter_dims_to_operand_dims))
    dnums = ScatterDimensionNumbers(
        update_window_dims=update_window_dims,
        inserted_window_dims=inserted_window_dims,
        scatter_dims_to_operand_dims=scatter_dims_to_operand_dims)
    return scatter_op(
      operand, indices, updates, dnums,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode), 0


  # see the third case in _gather_batching_rule for comparison and comments
  indices = batching.bdim_at_front(indices, indices_bdim, size)

  count_shape = list(indices.shape)
  count_shape[-1] = 1
  counts = lax.broadcasted_iota(indices.dtype, tuple(count_shape), 0)
  indices = lax.concatenate([counts, indices], len(count_shape) - 1)

  update_window_dims = tuple(np.add(1, dimension_numbers.update_window_dims))
  inserted_window_dims = (0,) + tuple(np.add(1, dimension_numbers.inserted_window_dims))
  scatter_dims_to_operand_dims = (0,) + tuple(np.add(1, dimension_numbers.scatter_dims_to_operand_dims))

  dnums = ScatterDimensionNumbers(
      update_window_dims=update_window_dims,
      inserted_window_dims=inserted_window_dims,
      scatter_dims_to_operand_dims=scatter_dims_to_operand_dims)
  return scatter_op(
      operand, indices, updates, dnums,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode), 0
