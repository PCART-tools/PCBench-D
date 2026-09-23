@tf_export('__internal__.mixed_precision.register_loss_scale_wrapper', v1=[])
def register_loss_scale_wrapper(optimizer_cls, wrapper_cls):
  """Registers a loss scale optimizer wrapper.

  `tf.compat.v1.mixed_precision.enable_mixed_precision_graph_rewrite`
  automatically wraps an optimizer with an optimizer wrapper that performs loss
  scaling. This function registers a `(base_optimizer, wrapper_optimizer)` pair
  that is used by `enable_mixed_precision_graph_rewrite`, where
  `wrapper_optimizer` wraps a `base_optimizer` and applies loss scaling.

  Args:
    optimizer_cls: A base optimizer class, e.g. `tf.keras.optimizers.Optimizer`.
    wrapper_cls: A wrapper that wraps `optimizer_cls` and applies loss scaling,
      e.g. `tf.compat.v1.keras.mixed_precision.LossScaleOptimizer`. The
      constructor should take two arguments: The inner optimizer and a
      `tf.compat.v1.mixed_precision.LossScale`.
  """
  _REGISTERED_WRAPPER_OPTIMIZER_CLS[optimizer_cls] = wrapper_cls
