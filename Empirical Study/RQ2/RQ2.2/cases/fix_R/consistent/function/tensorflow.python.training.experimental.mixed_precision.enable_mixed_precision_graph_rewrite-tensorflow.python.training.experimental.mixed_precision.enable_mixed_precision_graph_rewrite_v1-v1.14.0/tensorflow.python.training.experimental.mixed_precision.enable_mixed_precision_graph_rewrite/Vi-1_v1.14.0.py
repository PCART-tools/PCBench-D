@tf_export(v1=['train.experimental.enable_mixed_precision_graph_rewrite'])
def enable_mixed_precision_graph_rewrite(opt, loss_scale='dynamic'):
  """Enable mixed precision via a graph rewrite.

  Mixed precision is the use of both float16 and float32 when training a model,
  and is used to make the model run faster. This function will use mixed
  precision to speed up the execution time of your model when run on a GPU. It
  does this by changing the dtype of certain operations in the graph from
  float32 to float16.

  This function additionally wraps an Optimizer with a LossScaleOptimizer, which
  is required to prevent underflow in the float16 tensors during the backwards
  pass. An optimizer must be passed to this function, which will then be wrapped
  to use loss scaling.

  When this function is used, gradients should only be computed and applied with
  the returned optimizer, either by calling `opt.minimize()` or
  `opt.compute_gradients()` followed by `opt.apply_gradients()`. Gradients
  should not be computed with `tf.gradients` or `tf.GradientTape`. This is
  because the returned optimizer will apply loss scaling, and
  `tf.gradients`/`tf.GradientTape` will not. If you do directly use
  `tf.gradients` or `tf.GradientTape`, your model may train to a worse quality.

  When eager execution is enabled, the mixed precision graph rewrite is only
  enabled within `tf.function`s, as outside `tf.function`s, there is no graph.

  When enabled, mixed precision is only used on Volta GPUs and above. The parts
  of the graph on CPUs and TPUs are untouched by the graph rewrite.

  Args:
    opt: An instance of a `tf.keras.optimizers.Optimizer` or a
      `tf.train.Optimizer`.
    loss_scale: Either an int/float, the string "dynamic", or an instance of a
      `tf.train.experimental.LossScale`. The loss scale to use. It is
      recommended to keep this as its default value of "dynamic".

  Returns:
    A version of `opt` that will use loss scaling to prevent underflow.
  """
  # TODO(reedwm): If a ConfigProto is passed to Session, either assert that
  # auto_mixed_precision is on or turn it on for the user.
  if mixed_precision_global_state.non_mixed_precision_session_created:
    # TODO(reedwm): Give the stacktrace of the existing Sessions. And if the
    # Sessions have already been closed, do not raise this error message.
    tf_logging.warn('You already have existing Sessions that do not use mixed '
                    'precision. enable_mixed_precision_graph_rewrite() will '
                    'not affect these Sessions.')
  opt = _wrap_optimizer(opt, loss_scale)
  config.set_optimizer_experimental_options({'auto_mixed_precision': True})
  mixed_precision_global_state.mixed_precision_is_enabled = True
  return opt
