def _compute_gradients_until_finite(
    distribution, loss_scale_gradient_tapes, loss_scale, target, sources,
    output_gradients, unconnected_gradients):
  """Compute gradients and update the loss scale until the gradients are finite.

  This must be called in a cross-replica context.

  This is a function instead of a method of LossScaleGradientTape, as the `self`
  parameter would be meaningless. There is one LossScaleGradientTape per
  replica, but this function is called once total (not per replica), so there
  cannot be a singular `self` parameter.

  Args:
    distribution: The distribution strategy in effect.
    loss_scale_gradient_tapes: A PerReplica value of LossScaleGradientTapes.
      Contains the LossScaleGradientTape of each replica.
    loss_scale: The loss scale to use to scale the loss and unscale the
      gradient.
    target: a list or nested structure of Tensors or Variables to be
      differentiated.
    sources: a list or nested structure of Tensors or Variables. `target` will
      be differentiated against elements in `sources`.
    output_gradients: Passed to GradientTape.gradient
    unconnected_gradients: Pass to GradientTape.gradient.

  Returns:
    The gradients of `target` with respect to `sources`.
  """
  # Autograph cannot convert this function, so we must use an explicit
  # tf.while_loop.
  # TODO(b/143572314): Fix Autograph so that it can convert this function, then
  # replace the tf.while_loop with a Python while loop.

  # For convenience, we only deal with flattened sources
  flattened_sources = nest.flatten(sources)

  # Define the initial loop variables of the while loop.

  # Dummy value for initial_grads. The first iteration of the loop will
  # overwrite `grads` to the actual gradients.
  initial_grads = flattened_sources
  if distribution_strategy_context.has_strategy():
    # A while_loop requires the initial values to have the same types as the
    # return values from the body. However, 'initial_grads' may have type
    # 'DistributionVariable', while body returns a 'PerReplica'. While both
    # types subclass 'DistributedValues', while_loop will still throw an error.
    # So we convert 'initial_grads' to be PerReplica values.
    # TODO(b/146084534): Once the bug is fixed, remove this special case.
    initial_grads = _convert_to_per_replicas(distribution, initial_grads)
  initial_ready_to_update = False
  initial_is_first_iteration = True

  def cond(grads, ready_to_update, is_first_iteration):
    """The condition of the while loop."""
    del grads
    # Equivalent to:
    # `is_first_iteration or (not ready_to_update and loss_scale() > 1)`
    return math_ops.logical_or(
        is_first_iteration,
        math_ops.logical_and(
            math_ops.logical_not(ready_to_update),
            math_ops.greater(loss_scale(), 1)))

  # Boolean list specifying whether each gradient is None or not. Set by body().
  is_nones = []

  def body(grads, ready_to_update, is_first_iteration):
    """The body of the while loop."""
    del grads, ready_to_update, is_first_iteration
    def replica_fn(gradient_tape, target, flattened_sources, output_gradients,
                   initial_grads):
      """Scales the loss, computes the gradients, and unscales the gradients."""
      loss_scale_val = loss_scale()
      with gradient_tape:  # re-enter gradient tape so it sees the loss scaling
        scaled_target = nest.map_structure(
            lambda t: t * math_ops.cast(loss_scale_val, t.dtype), target)
      scaled_grads = super(LossScaleGradientTape, gradient_tape).gradient(
          scaled_target, flattened_sources, output_gradients,
          unconnected_gradients)

      is_nones[:] = [g is None for g in scaled_grads]
      inv_loss_scale = 1.0 / loss_scale_val
      grads = []  # The unscaled gradients
      for g, initial_grad in zip(scaled_grads, initial_grads):
        if g is not None:
          # We call ensure_shape as shape information can be lost for certain
          # ops, such as tf.transpose, if the op is called in a tf.function and
          # has inputs created outside the tf.function.
          # TODO(b/132092188): Remove ensure_shape call after this has been
          # fixed.
          g = array_ops.ensure_shape(g, initial_grad.shape)
          grads.append(g * math_ops.cast(inv_loss_scale, g.dtype))
        else:
          # We cannot return None from a tf.while_loop, so we pass a dummy
          # tensor instead. We use initial_grad as a dummy tensor as it has the
          # correct shape and dtype. We replace it with None outside the while
          # loop.
          grads.append(initial_grad)
      return grads

    # Switch to a replica-context to compute gradients once per replica.
    grads = distribution.run(
        replica_fn,
        args=(loss_scale_gradient_tapes, target, flattened_sources,
              output_gradients, initial_grads))
    # Check for non-finite gradients possibly resulting from scaling
    _, ready_to_update = loss_scale.update(grads)
    is_first_iteration = False
    return grads, ready_to_update, is_first_iteration

  grads, _, _ = control_flow_ops.while_loop(
      cond, body, [initial_grads, initial_ready_to_update,
                   initial_is_first_iteration],
      )
  grads = [None if is_none else g for g, is_none in zip(grads, is_nones)]
  grads = nest.pack_sequence_as(sources, grads)
  return grads
