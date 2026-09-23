def _block_copy(
    block_spec: core.BlockSpec,
    ref: REF,
    allocation: Optional[PipelineAllocation],
    buffers: PipelineBuffer,
    accum_allocation: Optional[PipelineAllocation] = None,
    accum_buffers: Optional[PipelineBuffer] = None,
    *,
    indices: tuple[
        GridIndices,
        GridIndices,
        GridIndices,
    ],
    is_input: bool,
    is_wait: bool,
    force_copy: Optional[Union[jax.Array, bool]] = None,
    force_skip: Optional[Union[jax.Array, bool]] = None,
):
  """General purpose input/output block copys.

  Basic flow:

  - Wait on input copy if previous block spec was different.
  - Start input copy if block spec is changing and it's not the last step.
  - Wait on output copy if previous block spec was different.
  - Start output copy if block spec is changing or is last step.

  The step constraints are enforced with force_copy and caller conds.

  Args:
    block_spec: Block spec.
    ref: HBM ref.
    allocation: VMEM ref and semaphore. If this is None it means the source refs
      are already in VMEM and we can avoid copy operations.
    buffers: Current and next buffer indices.
    accum_allocation: Accumulator VMEM ref and semaphore.
    accum_buffers: Accumulator current and next buffer indices.
    indices: Current grid indices.
    is_input: True if is input copy.
    is_wait: True if we want to wait on instead of start a copy.
    force_copy: Force copy if this condition is True. force_skip overrides this.
    force_skip: Force skipping the operation if this condition is True.

  Returns:
    Current and next buffer indices, swapped if a copy was started.
  """
  if allocation is None:
    # Has existing allocation.
    return buffers
  (vmem_ref, sem) = allocation.vmem_ref, allocation.semaphore
  (prev_indices, curr_indices, next_indices) = indices

  prev_dma_slice = _run_block_spec(block_spec, prev_indices)
  dma_slice = _run_block_spec(block_spec, curr_indices)
  next_dma_slice = _run_block_spec(block_spec, next_indices)

  prev_dma_slice_changed = _dma_slice_not_equal(prev_dma_slice, dma_slice)
  dma_slice_is_changing = _dma_slice_not_equal(dma_slice, next_dma_slice)

  buffer, next_buffer = buffers.current, buffers.next
  if is_input:
    if is_wait:
      # We wait for inputs of the current body iteration.
      used_dma_slice = dma_slice
      used_buffer = buffer
    else:
      # We send to the next ones.
      used_dma_slice = next_dma_slice
      used_buffer = next_buffer
  else:
    if is_wait:
      # We wait for the outputs of the previous body iteration.
      used_dma_slice = prev_dma_slice
      used_buffer = next_buffer
    else:
      # We send the current ones.
      used_dma_slice = dma_slice
      used_buffer = buffer

  if is_input:
    from_ref = ref.at[used_dma_slice]
    to_ref = vmem_ref.at[used_buffer]
  else:
    from_ref = vmem_ref.at[used_buffer]
    to_ref = ref.at[used_dma_slice]

  async_copy = tpu_primitives.make_async_copy(
      from_ref,
      to_ref,
      sem,
  )

  if is_wait:
    cond = prev_dma_slice_changed
    do_fn = async_copy.wait
    advance_buffers = False
  else:
    cond = dma_slice_is_changing
    do_fn = async_copy.start
    advance_buffers = True

  if force_copy is not None:
    cond = jnp.logical_or(cond, force_copy)
  if force_skip is not None:
    cond = jnp.logical_and(cond, jnp.logical_not(force_skip))

  def do_and_advance_buffers():
    if accum_allocation is not None:
      with tpu_primitives.trace("ep_accum_copy"):
        accum_dtype = jnp.float32
        if vmem_ref.dtype == jnp.int32:
          accum_dtype = jnp.int32
        accum_vmem_ref = accum_allocation.vmem_ref
        vmem_ref[used_buffer] = (
            vmem_ref[used_buffer].astype(accum_dtype)
            + accum_vmem_ref[accum_buffers.current].astype(accum_dtype)
        ).astype(vmem_ref.dtype)

    do_fn()
    if advance_buffers:
      return PipelineBuffer(next_buffer, buffer)
    return buffers

  return lax.cond(cond, do_and_advance_buffers, lambda: buffers)
