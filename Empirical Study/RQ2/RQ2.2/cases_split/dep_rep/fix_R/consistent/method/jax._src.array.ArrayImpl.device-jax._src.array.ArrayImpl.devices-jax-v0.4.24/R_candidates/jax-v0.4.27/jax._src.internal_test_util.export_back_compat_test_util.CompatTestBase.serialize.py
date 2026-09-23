  def serialize(self,
                func: Callable, data: CompatTestData, *,
                polymorphic_shapes: Sequence[str] | None = None,
                allow_unstable_custom_call_targets: Sequence[str] = ()
                ) -> tuple[bytes, str, int, int]:
    """Serializes the test function.

    Args:
      func: the function to serialize
      polymorphic_shapes: the polymorphic_shapes to use for serialization
      allow_unstable_custom_call_targets: whether to allow additional
        custom call targets besides those known as stable.

    Returns: a tuple with the (a) serialization, (b) the module contents as
      a string (for debugging), (c) the module serialization version,
      (d) the number of devices for which the module was serialized.
    """
    # Use the native exporter, to make sure we get the proper serialization.
    args_specs = export.symbolic_args_specs(data.inputs, polymorphic_shapes)
    exported = export.export(
      jax.jit(func),
      lowering_platforms=(self.default_jax_backend(),),
      disabled_checks=tuple(
        export.DisabledSafetyCheck.custom_call(target)
        for target in allow_unstable_custom_call_targets)
    )(*args_specs)

    module_str = str(exported.mlir_module())
    serialized = exported.mlir_module_serialized
    module_version = exported.mlir_module_serialization_version
    nr_devices = exported.nr_devices
    return serialized, module_str, module_version, nr_devices
