@dataclasses.dataclass(frozen=True)
class LoweringParameters:
  # A mapping between primitives and user-defined LoweringRules.
  # When lowering a primitive, give priorioty to the rule in this map over
  # existing Jax rules.
  override_lowering_rules: tuple[tuple[core.Primitive, LoweringRule]] | None = None

  # The current lowering platforms, a non-empty tuple containing some of
  # 'cpu', 'cuda', 'rocm', 'tpu'. If the tuple has multiple entries we are
  # doing multi-platform lowering, otherwise it can specify cross-platform
  # lowering. The value None specifies the default lowering platform.
  # This is used only in export and jax2tf.
  platforms: tuple[str, ...] | None = None

  # Signals that the entire computation being lowered operates on global
  # constants. This will result in adding jax.global_constant attributes
  # to the arguments of all functions that are created, e.g., floor_divide.
  # This is used only in export and jax2tf in presence of shape polymorphism
  # or multi-platform lowering.
  global_constant_computation: bool = False

  # TODO(b/302258959): in JAX native execution we cannot lower the tokens
  # to stablehlo.token for the top-level function, due to runtime limitations.
  # Instead, we use dummy bool[0] arrays. This is controlled by setting
  # replace_tokens_with_dummy to True (default). However, when exporting StableHLO
  # we can use real tokens, because the resulting StableHLO will not be
  # executed directly, but will be embedded as an inner function in a larger
  # JAX or TensorFlow program. In these cases, replace_tokens_with_dummy must
  # be set to False (for serialization versions >= 9).
  # Once the PJRT is extended to use tokens, we can use tokens even in the
  # native execution (and we can remove this parameter).
  replace_tokens_with_dummy: bool = True
